"""
Week 5 — Structured output with instructor + Pydantic.

This is exactly the pattern used in reasoning.py.
"""

import instructor
from openai import OpenAI
from pydantic import BaseModel, Field

raw_client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")
client = instructor.from_openai(raw_client, mode=instructor.Mode.JSON)
MODEL = "adrienbrault/saul-instruct-v1:Q8_0"


# --- Define the schema ---

class LegalFact(BaseModel):
    provision: str = Field(description="The legal provision, e.g. 'Article 1305'")
    summary: str = Field(description="One-sentence summary of the provision")
    applies_to: str = Field(description="Who or what this provision applies to")


class LegalAnalysis(BaseModel):
    topic: str = Field(description="The legal topic being analyzed")
    key_facts: list[LegalFact] = Field(description="The key legal facts and provisions")
    conclusion: str = Field(description="The overall legal conclusion")
    confidence: float = Field(description="Confidence from 0.0 to 1.0", ge=0.0, le=1.0)


# --- Call with structured output ---

result = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": "You are a Philippine legal expert. Analyze legal topics precisely.",
        },
        {
            "role": "user",
            "content": "Analyze the legal requirements for a valid contract under Philippine law.",
        },
    ],
    response_model=LegalAnalysis,
    max_tokens=500,
)

print("=== Structured Legal Analysis ===\n")
print(f"Topic: {result.topic}")
print(f"Confidence: {result.confidence:.2f}\n")
print("Key Facts:")
for i, fact in enumerate(result.key_facts, 1):
    print(f"  [{i}] Provision: {fact.provision}")
    print(f"      Summary: {fact.summary}")
    print(f"      Applies to: {fact.applies_to}")
print(f"\nConclusion: {result.conclusion}")

print("\n--- Raw Python object ---")
print(result.model_dump_json(indent=2))

print("\n--- Why this matters ---")
print("result.confidence is a float, not a string.")
print("result.key_facts is a list, not text to parse.")
print("If the model outputs invalid JSON, instructor retries automatically.")
print("This is how reasoning.py gets ReasoningResult as a typed Python object.")
