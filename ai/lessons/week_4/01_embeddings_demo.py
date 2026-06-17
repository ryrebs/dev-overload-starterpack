"""
Week 4 — Embeddings: visualize what semantic similarity looks like in vector space.

Requires bge-m3 running via Ollama.
"""

import numpy as np
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")


def embed(texts: list[str]) -> np.ndarray:
    response = client.embeddings.create(model="bge-m3", input=texts)
    return np.array([item.embedding for item in response.data])


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def similarity_matrix(texts: list[str]) -> np.ndarray:
    vecs = embed(texts)
    n = len(texts)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            matrix[i, j] = cosine_similarity(vecs[i], vecs[j])
    return matrix


if __name__ == "__main__":
    print("=== Embedding Similarity Demo ===\n")
    print("Embedding 6 texts into 1024-dimensional vectors...")

    legal_texts = [
        "The accused has the right to remain silent.",
        "A criminal defendant has the right against self-incrimination.",
        "Everyone is presumed innocent until proven guilty.",
        "Property can be transferred by deed or contract.",
        "The contract must be in writing to be enforceable.",
        "Ownership of land requires a certificate of title.",
    ]

    matrix = similarity_matrix(legal_texts)

    print("\nCosine Similarity Matrix (1.0 = identical, 0.0 = unrelated):\n")
    labels = [t[:35] + "..." for t in legal_texts]
    col_width = 8

    # Header
    print(f"{'':40s}", end="")
    for i in range(len(legal_texts)):
        print(f"T{i+1:6s}", end="")
    print()

    for i, (label, row) in enumerate(zip(labels, matrix)):
        print(f"T{i+1}: {label:38s}", end="")
        for val in row:
            bar = "█" * int(val * 5)
            print(f"{val:.2f}  ", end="")
        print()

    print("\nMost similar pairs:")
    pairs = []
    for i in range(len(legal_texts)):
        for j in range(i+1, len(legal_texts)):
            pairs.append((matrix[i, j], i, j))
    pairs.sort(reverse=True)

    for sim, i, j in pairs[:3]:
        print(f"  {sim:.3f}: [{i+1}] {legal_texts[i][:50]}")
        print(f"         [{j+1}] {legal_texts[j][:50]}")

    print("\nLeast similar pairs:")
    for sim, i, j in pairs[-3:]:
        print(f"  {sim:.3f}: [{i+1}] {legal_texts[i][:50]}")
        print(f"         [{j+1}] {legal_texts[j][:50]}")

    print("\nObservation: legal rights texts cluster together,")
    print("property/contract texts cluster separately.")
