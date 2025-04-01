import os
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from typing_extensions import List, TypedDict
from langgraph.graph import START, END, StateGraph, MessagesState
from langchain_chroma import Chroma
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import Literal
from typing_extensions import Annotated
from langchain_core.tools import tool


# Embedding model (Make sure ollama is runnning and qwen2.5:7b is pulled)
embeddings = OllamaEmbeddings(model="qwen2.5:7b")

# Chroma for local vector store
vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",
)

llm = init_chat_model("qwen2.5:7b", model_provider="ollama")


# Specify an ID for the thread
config = {"configurable": {"thread_id": "abc123"}}


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


def init_source():
    docs = load_source()
    docs_splitted = split_source(docs)
    store_doc(docs_splitted, False)


@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related"""

    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )

    return serialized, retrieved_docs


## Setting this function allows the flow to either
## respond directly to the query or send a query again.
# Step 1: Generate an AIMessage that may include a tool-call to be sent.
def query_or_respond(state: MessagesState):
    """Generate tool call for retrieval or respond."""

    ## Decide if this message requires a tool call.
    ## The larger the model the better.
    ## The example from where this tutorial have been taken
    ## might use different model, hence different expected results.
    ## So play with the message until it gives you expected
    ## on tool calling.
    llm_with_tools = llm.bind_tools([retrieve])
    response = llm_with_tools.invoke(state["messages"])

    ## Sample tool call  was invoke:
    ## tool_calls=[{'name': 'retrieve',
    #       'args': {'query': 'task decomposition'},
    #       'id': '529e3bd3-785a-40e1-906d-9ca12c616bd0',
    #       'type': 'tool_call'}]

    # MessagesState appends messages to state instead of overwriting
    return {"messages": [response]}


# Step 3: Generate a response using the retrieved content.
def generate(state: MessagesState):
    ## If there is a tool call that was sent,
    ## ToolMessage contains the data from the vector database
    ## we'll use this as context for the question.
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]
    docs_content = "\n\n".join(doc.content for doc in tool_messages)

    # Format into prompt
    system_message_content = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        f"{docs_content}"
    )

    # Combined message from state: ai + human
    conversation_messages = [
        message
        for message in state["messages"]
        if message.type in ("human", "system")
        or (message.type == "ai" and not message.tool_calls)
    ]

    # Complete prompt without the tool message: prompt + ai message + human message
    prompt = [SystemMessage(system_message_content)] + conversation_messages

    # Run
    response = llm.invoke(prompt)
    return {"messages": [response]}


def save_graph(graph):
    with open("grap_rag.png", "wb+") as im:
        im.write(graph.get_graph().draw_mermaid_png())


if __name__ == "__main__":
    """Summary
    0. Setup ollama on docker and pull model. Where using qwen2.5:7b
    1. Choose your data source and use a loader for that data.
    2. Choose your embedding models since data needs to be stored in format
    that is efficient is more suitable for AI or LLM, that's why where using
    vector databases.
    3. We need to split data into chunks before storing it to the vector db (Chromadb)
    4. After splitting, we use an embedding model (qwen2.5:7b) to create numerical vector representations
    of our data (vectors)
    5. Setup our questions.
    6. We use the langgraph to initiate the process.
    8. Retrieve will be used as a tool to get all the information necessary to answery our question stored in Vector database
    9. query_or_respond decides if the process can respond directly or needs additional query.
    10.Storing chat history with sqlite

    """

    ## Initialize our knowledge source
    # init_source()

    ## Setup persistence
    conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
    memory = SqliteSaver(conn)
    config = {"configurable": {"thread_id": "1"}}

    # Step 2: Execute the retrieval.
    tools = ToolNode([retrieve])

    graph_builder = StateGraph(MessagesState)
    graph_builder.add_node(query_or_respond)
    graph_builder.add_node(tools)
    graph_builder.add_node(generate)

    graph_builder.set_entry_point("query_or_respond")
    graph_builder.add_conditional_edges(
        "query_or_respond",
        tools_condition,
        {END: END, "tools": "tools"},
    )
    graph_builder.add_edge("tools", "generate")
    graph_builder.add_edge("generate", END)

    graph = graph_builder.compile(checkpointer=memory)
    save_graph(graph)

    ## A tool call with relevant info is returned as ToolMessage,
    ## and that will be used as the context for answering our query.

    ## After setting up persistence
    ## We send a follow question based on the previous question.
    q0 = "Hi"  # without invoking a tool call.
    q1 = "What is task decomposition? and look up some available resources"
    q2 = "Can you look up ways on doing it?"
    for step in graph.stream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": q2,  # Assuming q1 is already sent and persistence is setup.
                }
            ]
        },
        stream_mode="values",
        config=config,
    ):
        step["messages"][-1].pretty_print()
