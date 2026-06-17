"""
Week 5 — Zero-shot vs. few-shot vs. chain-of-thought prompting.

Run all three on the same question and compare the output.
"""

from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")
MODEL = "adrienbrault/saul-instruct-v1:Q8_0"

QUESTION = "Can a minor enter into a binding contract in the Philippines?"


def call(messages: list[dict], label: str):
    print(f"\n{'='*60}")
    print(f"APPROACH: {label}")
    print(f"{'='*60}")
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=250,
        temperature=0.1,
    )
    print(response.choices[0].message.content)


# 1. Zero-shot: just ask
call(
    messages=[{"role": "user", "content": QUESTION}],
    label="ZERO-SHOT",
)

# 2. Few-shot: provide examples
call(
    messages=[
        {
            "role": "user",
            "content": (
                "Q: Can a married person enter into a contract without spousal consent?\n"
                "A: Under Article 1403 of the Civil Code, contracts entered into without "
                "the consent of the spouse in cases required by law are voidable. "
                "The non-consenting spouse may annul the contract.\n\n"
                "Q: Is a contract for an illegal purpose valid?\n"
                "A: No. Under Article 1306, contracts whose cause, object, or purpose is "
                "contrary to law, morals, good customs, public order, or public policy "
                "are void from the beginning.\n\n"
                f"Q: {QUESTION}\n"
                "A:"
            )
        }
    ],
    label="FEW-SHOT",
)

# 3. Chain-of-thought: ask to reason step by step
call(
    messages=[
        {
            "role": "system",
            "content": "You are a Philippine legal expert. Think through legal questions step by step.",
        },
        {
            "role": "user",
            "content": (
                f"{QUESTION}\n\n"
                "Think through this step by step:\n"
                "1. What does Philippine law say about capacity to contract?\n"
                "2. What is the legal status of minors?\n"
                "3. What happens to contracts entered into by minors?\n"
                "4. Are there exceptions?\n"
                "Conclusion:"
            ),
        }
    ],
    label="CHAIN-OF-THOUGHT",
)

print("\n" + "="*60)
print("OBSERVATION:")
print("Zero-shot: model uses its training knowledge, may be vague")
print("Few-shot: model follows the pattern from examples, more structured")
print("CoT: model reasons explicitly, usually most accurate for complex questions")
