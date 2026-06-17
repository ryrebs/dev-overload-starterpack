"""
Week 5 — Few-shot prompt builder for legal Q&A.

Build a reusable few-shot prompt template from examples in your corpus.
"""

from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")
MODEL = "adrienbrault/saul-instruct-v1:Q8_0"

# Few-shot examples — question + ideal answer pairs
FEW_SHOT_EXAMPLES = [
    {
        "q": "What is the age of majority in the Philippines?",
        "a": "Under Article 234 of the Civil Code, majority commences at the age of eighteen years. Emancipation takes place upon attaining this age.",
    },
    {
        "q": "What are the essential elements of a contract?",
        "a": "Under Article 1318 of the Civil Code, there is no contract unless three requisites concur: (1) consent of the contracting parties; (2) object certain which is the subject matter; and (3) cause of the obligation.",
    },
    {
        "q": "Is an accused person presumed guilty or innocent?",
        "a": "Under Article III Section 14(2) of the 1987 Constitution, in all criminal prosecutions, the accused shall be presumed innocent until the contrary is proved beyond reasonable doubt.",
    },
]


def build_few_shot_prompt(question: str, examples: list[dict]) -> str:
    """Build a prompt with examples followed by the actual question."""
    lines = []
    for ex in examples:
        lines.append(f"Q: {ex['q']}")
        lines.append(f"A: {ex['a']}")
        lines.append("")
    lines.append(f"Q: {question}")
    lines.append("A:")
    return "\n".join(lines)


def few_shot_query(question: str, n_examples: int = 3) -> str:
    examples = FEW_SHOT_EXAMPLES[:n_examples]
    prompt = build_few_shot_prompt(question, examples)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a Philippine legal expert. Answer concisely, citing specific articles."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,
        temperature=0.1,
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    print("=== Few-Shot Legal Q&A ===\n")

    test_questions = [
        "Can a minor enter into a contract?",
        "What rights does an accused have during trial?",
        "How does one acquire property ownership?",
    ]

    for q in test_questions:
        print(f"Q: {q}")
        answer = few_shot_query(q, n_examples=2)
        print(f"A: {answer}\n")
