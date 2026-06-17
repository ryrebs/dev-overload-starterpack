"""
Week 4 — Minimal end-to-end RAG pipeline.

The simplest possible version of what the full project does:
Embed → Store → Retrieve → Reason.
"""

import chromadb
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")
EMBED_MODEL = "bge-m3"
LLM_MODEL = "adrienbrault/saul-instruct-v1:Q8_0"


def embed(texts: list[str]) -> list[list[float]]:
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [item.embedding for item in resp.data]


def build_index(documents: list[str], sources: list[str]):
    chroma = chromadb.Client()
    col = chroma.create_collection("rag_demo", metadata={"hnsw:space": "cosine"})
    embeddings = embed(documents)
    col.add(
        documents=documents,
        embeddings=embeddings,
        ids=[f"doc_{i}" for i in range(len(documents))],
        metadatas=[{"source": s} for s in sources],
    )
    return col


def retrieve(col, question: str, k: int = 3) -> list[dict]:
    q_embed = embed([question])[0]
    results = col.query(query_embeddings=[q_embed], n_results=k,
                        include=["documents", "metadatas", "distances"])
    return [
        {
            "text": doc,
            "source": meta["source"],
            "score": round(1 - dist, 4),
        }
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]


def reason(question: str, chunks: list[dict]) -> str:
    evidence = "\n\n".join(
        f"[{i+1}] {c['source']}: {c['text']}"
        for i, c in enumerate(chunks)
    )
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a legal assistant. Answer only from the provided evidence. Cite your sources.",
            },
            {
                "role": "user",
                "content": f"EVIDENCE:\n{evidence}\n\nQUESTION: {question}",
            },
        ],
        max_tokens=300,
        temperature=0.1,
    )
    return response.choices[0].message.content


def rag_query(col, question: str) -> dict:
    chunks = retrieve(col, question)
    answer = reason(question, chunks)
    return {"question": question, "answer": answer, "sources": [c["source"] for c in chunks]}


if __name__ == "__main__":
    print("=== Simple RAG Pipeline ===\n")

    # Small corpus — the real project uses parsed PDFs/HTML
    docs = [
        "No person shall be held to answer for a criminal offense without due process of law.",
        "The accused shall be presumed innocent until the contrary is proved.",
        "Majority commences at the age of eighteen years.",
        "A contract is a meeting of minds between two persons.",
        "There is no contract unless there is consent, object, and cause.",
    ]
    sources = ["const.md", "const.md", "civil.md", "civil.md", "civil.md"]

    print("Building index...")
    col = build_index(docs, sources)
    print(f"Indexed {len(docs)} documents.\n")

    questions = [
        "Is the accused presumed guilty or innocent?",
        "At what age does a person become an adult?",
        "What three things does a contract need?",
    ]

    for q in questions:
        print(f"Q: {q}")
        result = rag_query(col, q)
        print(f"A: {result['answer']}")
        print(f"Sources: {result['sources']}")
        print()
