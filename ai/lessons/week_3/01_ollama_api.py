"""
Week 3 — Call Ollama's OpenAI-compatible API directly.

Inspect request/response structure. Understand what happens under the hood
when reasoning.py calls the LLM.
"""

import json
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")
MODEL = "adrienbrault/saul-instruct-v1:Q8_0"


def basic_completion():
    print("=== Basic Chat Completion ===\n")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful legal assistant."},
            {"role": "user", "content": "What is habeas corpus? One sentence."},
        ],
        max_tokens=100,
        temperature=0.1,
    )
    print(f"Response: {response.choices[0].message.content}")
    print(f"\nUsage:")
    print(f"  prompt_tokens:     {response.usage.prompt_tokens}")
    print(f"  completion_tokens: {response.usage.completion_tokens}")
    print(f"  total_tokens:      {response.usage.total_tokens}")
    print(f"\nFinish reason: {response.choices[0].finish_reason}")


def streaming_completion():
    print("\n=== Streaming Completion ===\n")
    print("Tokens arriving one at a time: ", end="", flush=True)
    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": "Name three fundamental rights in one short sentence each."},
        ],
        max_tokens=150,
        temperature=0.1,
        stream=True,
    )
    full_text = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        print(delta, end="", flush=True)
        full_text += delta
    print(f"\n\nTotal characters: {len(full_text)}")


def list_models():
    print("\n=== Available Models ===\n")
    models = client.models.list()
    for model in models.data:
        print(f"  {model.id}")


def embeddings_call():
    print("\n=== Embeddings ===\n")
    response = client.embeddings.create(
        model="bge-m3",
        input=["The accused has the right to counsel."],
    )
    vec = response.data[0].embedding
    print(f"Text: 'The accused has the right to counsel.'")
    print(f"Embedding dimensions: {len(vec)}")
    print(f"First 10 values: {[round(v, 4) for v in vec[:10]]}")
    print(f"Min: {min(vec):.4f} | Max: {max(vec):.4f}")


if __name__ == "__main__":
    basic_completion()
    streaming_completion()
    list_models()
    embeddings_call()
