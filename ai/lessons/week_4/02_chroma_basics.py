"""
Week 4 — Chroma: build a mini vector database, insert documents, query it.

This is a self-contained version of what index.py and retrieval.py do.
"""

import chromadb
import numpy as np
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")


def embed(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(model="bge-m3", input=texts)
    return [item.embedding for item in response.data]


def build_demo_collection():
    """Create an in-memory Chroma collection with legal document chunks."""

    # In-memory: doesn't persist (use PersistentClient for persistence)
    chroma = chromadb.Client()
    collection = chroma.create_collection(
        name="demo",
        metadata={"hnsw:space": "cosine"},
    )

    # Sample legal document chunks
    documents = [
        "Section 14. (1) No person shall be held to answer for a criminal offense without due process of law.",
        "Section 14. (2) In all criminal prosecutions, the accused shall be presumed innocent until the contrary is proved.",
        "Section 14. (3) The accused has the right to be heard by himself and counsel.",
        "Article 234. Emancipation takes place by the attainment of majority. Unless otherwise provided, majority commences at the age of eighteen years.",
        "Article 1305. A contract is a meeting of minds between two persons whereby one binds himself, with respect to the other, to give something or to render some service.",
        "Article 1318. There is no contract unless the following requisites concur: (1) Consent of the contracting parties; (2) Object certain which is the subject matter of the contract; (3) Cause of the obligation which is established.",
        "Article 712. Ownership is acquired by occupation and by intellectual creation. Ownership and other real rights over property are acquired and transmitted by law, by donation, by testate and intestate succession, and in consequence of certain contracts.",
    ]
    sources = [
        "constitution.md", "constitution.md", "constitution.md",
        "civil_code.md", "civil_code.md", "civil_code.md", "civil_code.md",
    ]

    print(f"Embedding {len(documents)} chunks...")
    embeddings = embed(documents)

    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(documents))],
        metadatas=[{"source": s} for s in sources],
    )

    print(f"Stored {collection.count()} chunks in Chroma.\n")
    return collection


def query_collection(collection, question: str, k: int = 3):
    print(f"Query: '{question}'")
    print(f"Searching top {k} chunks...\n")

    query_embedding = embed([question])[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    for i, (doc, meta, dist) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    )):
        # Chroma returns distance. Cosine distance = 1 - cosine_similarity.
        similarity = 1 - dist
        print(f"[{i+1}] score={similarity:.4f} | source={meta['source']}")
        print(f"     {doc[:120]}...")
        print()


if __name__ == "__main__":
    print("=== Chroma Vector Database Demo ===\n")

    collection = build_demo_collection()

    queries = [
        "What are the rights of an accused person?",
        "What is the age of majority?",
        "What makes a contract valid?",
        "How is property ownership transferred?",
    ]

    for q in queries:
        query_collection(collection, q, k=2)
        print("-" * 60)
