"""
Week 3 — Inspect model metadata via the Ollama API.

Shows what architecture information is available without downloading model weights.
"""

import subprocess
import json
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")


def list_local_models():
    print("=== Local Ollama Models ===\n")
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True, text=True
        )
        print(result.stdout)
    except FileNotFoundError:
        print("Ollama CLI not in PATH. Use: docker exec <container> ollama list")


def show_model_info(model_name: str):
    print(f"\n=== Model Info: {model_name} ===\n")
    try:
        result = subprocess.run(
            ["ollama", "show", model_name, "--modelfile"],
            capture_output=True, text=True
        )
        print(result.stdout[:2000])  # first 2000 chars of modelfile
    except FileNotFoundError:
        print(f"Try: docker exec <container> ollama show {model_name}")


def verify_embedding_dimensions():
    print("\n=== Verify Embedding Dimensions ===\n")
    test_texts = [
        "short",
        "a much longer piece of text with many words in it",
        "legal text: The accused has the right to due process under Article III.",
    ]
    for text in test_texts:
        response = client.embeddings.create(model="bge-m3", input=[text])
        vec = response.data[0].embedding
        print(f"  '{text[:40]:<40s}' → {len(vec)} dimensions")

    print("\nNote: embedding dimension is FIXED regardless of input length.")
    print("This is why embeddings work for similarity: every text maps to the same space.")


def compare_similar_vs_different():
    print("\n=== Cosine Similarity: Similar vs. Different Texts ===\n")
    import numpy as np

    def cosine_sim(a, b):
        a, b = np.array(a), np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    pairs = [
        ("rights of accused person", "due process rights defendant"),
        ("rights of accused person", "recipe for chicken adobo"),
        ("Article 3 Section 14", "constitutional rights criminal procedure"),
        ("habeas corpus", "right to counsel"),
    ]

    for text_a, text_b in pairs:
        resp = client.embeddings.create(model="bge-m3", input=[text_a, text_b])
        vec_a = resp.data[0].embedding
        vec_b = resp.data[1].embedding
        sim = cosine_sim(vec_a, vec_b)
        bar = "█" * int(sim * 20)
        print(f"  Similarity: {sim:.3f} {bar}")
        print(f"    A: '{text_a}'")
        print(f"    B: '{text_b}'")
        print()


if __name__ == "__main__":
    list_local_models()
    show_model_info("adrienbrault/saul-instruct-v1:Q8_0")
    verify_embedding_dimensions()
    compare_similar_vs_different()
