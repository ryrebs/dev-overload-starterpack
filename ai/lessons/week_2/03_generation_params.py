"""
Week 2 — Effect of generation parameters (temperature, top_p) on LLM output.

Run with Ollama running locally.
"""

from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")
MODEL = "adrienbrault/saul-instruct-v1:Q8_0"

PROMPT = "Complete this sentence about legal rights in one sentence: The accused has the right to"


def generate(temperature: float, top_p: float, label: str, n_samples: int = 3):
    print(f"\n{'='*60}")
    print(f"{label} (temperature={temperature}, top_p={top_p})")
    print(f"{'='*60}")
    for i in range(n_samples):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": PROMPT}],
            temperature=temperature,
            top_p=top_p,
            max_tokens=60,
        )
        print(f"[{i+1}] {response.choices[0].message.content.strip()}")


if __name__ == "__main__":
    print(f"Prompt: '{PROMPT}'")
    print("Generating 3 samples for each setting...\n")

    # Greedy (temperature=0): always picks highest probability token
    # Same result every time
    generate(temperature=0.0, top_p=1.0, label="GREEDY (temperature=0)", n_samples=3)

    # Low temperature: mostly deterministic, small variation
    generate(temperature=0.2, top_p=0.9, label="LOW TEMPERATURE (0.2)", n_samples=3)

    # Normal temperature: balanced exploration
    generate(temperature=0.7, top_p=0.9, label="NORMAL TEMPERATURE (0.7)", n_samples=3)

    # High temperature: creative / random
    generate(temperature=1.5, top_p=1.0, label="HIGH TEMPERATURE (1.5)", n_samples=3)

    print("\n" + "="*60)
    print("RECOMMENDATION FOR LEGAL REASONING:")
    print("Use temperature=0.1 to 0.3.")
    print("You want consistent, citation-accurate answers, not creative ones.")
    print("="*60)
