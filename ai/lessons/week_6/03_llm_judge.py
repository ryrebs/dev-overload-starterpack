"""
Week 6 — Use an LLM as a judge to score reasoning quality.

Compares the model's answer to expected keywords and scores 0-3.
"""

import json
import sys
from pathlib import Path
from openai import OpenAI

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from retrieval import retrieve
from reasoning import reason

client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")
JUDGE_MODEL = "adrienbrault/saul-instruct-v1:Q8_0"
GOLDEN_PATH = Path(__file__).parent / "golden.json"


def llm_judge(question: str, model_answer: str, expected_keywords: list[str]) -> dict:
    """
    Ask an LLM to score the answer 0-3.
    Returns {score, reasoning}.
    """
    keywords_str = ", ".join(expected_keywords) if expected_keywords else "N/A"

    prompt = f"""You are evaluating a legal AI assistant's answer.

Question: {question}

Model Answer: {model_answer}

Expected keywords/concepts that should appear: {keywords_str}

Score the answer from 0 to 3:
0 = Wrong or completely off-topic
1 = Partially correct but missing key information
2 = Correct and addresses the question
3 = Correct, cites specific legal provisions, well-reasoned

Respond with JSON: {{"score": <0-3>, "reasoning": "<one sentence why>"}}"""

    response = client.chat.completions.create(
        model=JUDGE_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.0,
    )

    text = response.choices[0].message.content.strip()
    try:
        # Extract JSON from the response
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            result = json.loads(text[start:end])
            return {"score": int(result.get("score", 0)), "reasoning": result.get("reasoning", "")}
    except (json.JSONDecodeError, ValueError):
        pass
    return {"score": 0, "reasoning": f"Could not parse judge output: {text[:100]}"}


def evaluate_reasoning(n_questions: int = 5):
    if not GOLDEN_PATH.exists():
        print("golden.json not found. Run 01_golden_dataset.py first.")
        return

    golden = json.loads(GOLDEN_PATH.read_text())
    questions = [q for q in golden if q["expected_established"]][:n_questions]

    print(f"Evaluating reasoning quality on {len(questions)} questions...\n")
    print("This will take a few minutes (one LLM call per question + one judge call).\n")

    scores = []
    for q in questions:
        print(f"Q: {q['question'][:60]}...")

        # Retrieve + reason
        chunks = retrieve(q["question"], k=5)
        result = reason(q["question"], chunks)

        # Judge
        judgment = llm_judge(q["question"], result.answer, q["expected_keywords"])
        scores.append(judgment["score"])

        print(f"  Established: {result.established}")
        print(f"  Answer (first 100 chars): {result.answer[:100]}...")
        print(f"  Judge score: {judgment['score']}/3 — {judgment['reasoning']}")
        print()

    avg_score = sum(scores) / len(scores) if scores else 0
    print(f"{'='*50}")
    print(f"Average judge score: {avg_score:.2f}/3.0")
    print(f"Score distribution: {dict(zip(*[[0,1,2,3],[scores.count(i) for i in range(4)]][::-1]))}")
    print(f"{'='*50}")

    if avg_score < 1.5:
        print("\nReasoning quality is low. Consider:")
        print("  - Improving the system prompt in reasoning.py")
        print("  - Increasing k (more evidence chunks)")
        print("  - Switching to a better reasoning model")
    elif avg_score < 2.5:
        print("\nReasoning quality is acceptable. Fine-tune the prompt.")
    else:
        print("\nReasoning quality is good.")


if __name__ == "__main__":
    evaluate_reasoning(n_questions=5)
