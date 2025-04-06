from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_chroma import Chroma


## Document - represents a piece of information
# page_content: a string representing the content;
# metadata: a dict containing arbitrary metadata;
# id: (optional) a string identifier for the document.
## Sample of generating a document
documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),
]

## Loaders - loads data from a source (web, text ,csv, pdf, etc..) into a document
file_path = "sample_data/nke-10k-2023.pdf"
loader = PyPDFLoader(file_path)


def store_docs(store, docs):
    vector_store.add_documents(docs)


def split_docs(docs):
    ## Text splitters to further split
    ## the documents into more documents based
    ## on the character size or chunk_size
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    all_splits = text_splitter.split_documents(docs)
    return all_splits


if __name__ == "__main__":
    ## Embeddings - store data as vectors.
    ## this way llms or embedding models
    ## can efficiently access related data
    embeddings = OllamaEmbeddings(model="qwen2.5:7b")
    ## Store the vectors in memory
    ## Takes too long on my setup
    ## switching to Chroma so we can invoke
    ## splitters and storing document only once
    vector_store = Chroma(
        collection_name="example_collection",
        embedding_function=embeddings,
        persist_directory="./chroma_langchain_db",
    )

    def initialize_store_data():
        # Loads 1 document per page
        docs = loader.load()

        # Split docs
        more_docs = split_docs(docs)

        ## Store vector locally with Chroma
        ## Store 10 docs for demo purposes
        store_docs(embeddings, more_docs[:10])

    # initialize_store_data()

    ## Then we can query for similiraty
    ## we can query similarity with scores or similarity
    ## with vectors. See docs.
    ## Returns Document/s related to our query
    results = vector_store.similarity_search("When was NIKE, Inc. incorporated?")

    # print(len(results))
    # print(results[0].metadata)

    results = vector_store.similarity_search_with_score(
        "When was NIKE, Inc. incorporated?"
    )
    print(len(results))
    print(results[3])
