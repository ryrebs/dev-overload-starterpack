def populate_store_with_examples():
    to_vectorize = [" ".join(example.values()) for example in query_examples]
    vector_store = Chroma.from_texts(
        to_vectorize,
        embeddings,
        metadatas=query_examples,
        collection_name="query_collection",
        persist_directory="./chroma_langchain_db",
    )

    return vector_store
