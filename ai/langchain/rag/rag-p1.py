import os
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from typing_extensions import List, TypedDict
from langgraph.graph import START, StateGraph
from langchain_chroma import Chroma

from typing import Literal

from typing_extensions import Annotated


class SearchQuery(TypedDict):
    """Search query."""

    query: Annotated[str, ..., "Search query to run."]
    section: Annotated[
        Literal["beginning", "middle", "end"],
        ...,
        "Section to query.",
    ]


## Use Langgraph
class State(TypedDict):
    question: str
    query: SearchQuery
    context: List[Document]
    answer: str


# Embedding model (Make sure ollama is runnning and llama3.2:1b is pulled)
embeddings = OllamaEmbeddings(model="llama3.2:1b")

# Chroma for local vector store
vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",
)


## Load the source or the data as documents
def load_source():
    # Only keep post title, headers, and content from the full HTML.
    bs4_strainer = bs4.SoupStrainer(
        class_=("post-title", "post-header", "post-content")
    )
    loader = WebBaseLoader(
        web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
        bs_kwargs={"parse_only": bs4_strainer},
    )
    docs = loader.load()
    assert len(docs) == 1

    return docs


## Split for documents into chunks for embedding and vector storage
## The amount of characters shoould fit into the model's context window
def split_source(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # chunk size (characters)
        chunk_overlap=200,  # chunk overlap (characters)
        add_start_index=True,  # track index in original document
    )
    all_splits = text_splitter.split_documents(docs)

    return all_splits


## Store the documents as vectors
def store_doc(all_splits, with_metadata=False):

    if with_metadata:
        total_documents = len(all_splits)
        third = total_documents // 3

        for i, document in enumerate(all_splits):
            if i < third:
                document.metadata["section"] = "beginning"
            elif i < 2 * third:
                document.metadata["section"] = "middle"
            else:
                document.metadata["section"] = "end"

    # Add the splitted docs
    vector_store.add_documents(documents=all_splits)


## Setup chat moddel
def get_chat_model():
    llm = init_chat_model("llama3.2:1b", model_provider="ollama")
    return llm


def create_message(question, context):
    return [
        (
            "system",
            """You are an assistant for question-answering tasks.
            Use the following pieces of retrieved context to answer the question.
            If you don't know the answer, just say that you don't know.
            Use three sentences maximum and keep the answer concise.""",
        ),
        ("human", f"My question is: {question}. The context is: {context}"),
    ]


def init_source():
    docs = load_source()
    docs_splitted = split_source(docs)
    store_doc(docs_splitted, True)


## Query analysis for adding filters
## Helping model rewrite queries for better results
def analyze_query(state: State):
    llm = get_chat_model()
    structured_llm = llm.with_structured_output(SearchQuery)
    query = structured_llm.invoke(state["question"])
    return {"query": query}


def retrieve(state: State):
    init_source()
    query = state["query"]
    retrieved_docs = vector_store.similarity_search(
        query["query"],
        filter={"section": query["section"]},
    )
    return {"context": retrieved_docs}


def generate(state: State):
    llm = get_chat_model()
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = create_message(state["question"], docs_content)
    response = llm.invoke(messages)
    return {"answer": response.content}


if __name__ == "__main__":
    """Summary
    0. Setup ollama on docker and pull model. Where using llama3.2:1b
    1. Choose your data source and use a loader for that data.
    2. Choose your embedding models since data needs to be stored in format
    that is efficient is more suitable for AI or LLM, that's why where using
    vector databases.
    3. We need to split data into chunks before storing it to the vector db (Chromadb)
    4. After splitting, we use an embedding model (llama3.2:1b) to create numerical vector representations
    of our data (vectors)
    5. Setup our questions.
    6. We use the langgraph to initiate the process.
    7. Analyze query, improves the query and adds metadata if necessary
    8. Retrieve will get all the information necessary to answery our question stored in Vector database
    9. Feed the context and question to LLM.
    10. Answer will be generated.

    """

    graph_builder = StateGraph(State).add_sequence([analyze_query, retrieve, generate])
    graph_builder.add_edge(START, "analyze_query")
    graph = graph_builder.compile()

    result = graph.invoke({"question": "What is Task Decomposition?"})

    # Sync
    # print(f'Context: {result["context"]}\n\n')
    # print(f'Answer: {result["answer"]}')

    # Streaming
    # for message, _ in graph.stream(
    #     {"question": "What is Task Decomposition?"}, stream_mode="messages"
    # ):
    #     print(message.content, end="")

    for step in graph.stream(
        {"question": "What is Task Decomposition according to the post end's section"},
        stream_mode="updates",
    ):
        print(f"{step}\n\n----------------\n")
