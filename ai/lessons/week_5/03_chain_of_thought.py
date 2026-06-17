"""
Week 5 — Chain-of-thought vs direct answer comparison.

Shows how CoT improves accuracy on multi-step legal reasoning questions.
"""

from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")
MODEL = "adrienbrault/saul-instruct-v1:Q8_0"

COMPLEX_QUESTION = (
    "A 17-year-old enters into a contract to buy a car worth 500,000 pesos. "
    "The seller is unaware of the buyer's age. Is the contract valid? "
    "What can each party do?"
)


def direct_answer(question: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a Philippine legal assistant."},
            {"role": "user", "content": question},
        ],
        max_tokens=200,
        temperature=0.1,
    )
    return response.choices[0].message.content


def chain_of_thought_answer(question: str) -> str:
    cot_prompt = f"""{question}

Think step by step:
Step 1: What is the legal capacity of a 17-year-old under Philippine law?
Step 2: What type of contract defect does this create?
Step 3: Who can raise the defect and how?
Step 4: What are the remedies available to each party?
Final Answer:"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a Philippine legal assistant. Reason through each step carefully."},
            {"role": "user", "content": cot_prompt},
        ],
        max_tokens=400,
        temperature=0.1,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print("QUESTION:")
    print(COMPLEX_QUESTION)

    print("\n" + "="*60)
    print("DIRECT ANSWER (no reasoning steps):")
    print("="*60)
    print(direct_answer(COMPLEX_QUESTION))

    print("\n" + "="*60)
    print("CHAIN-OF-THOUGHT (step by step reasoning):")
    print("="*60)
    print(chain_of_thought_answer(COMPLEX_QUESTION))

    print("\n" + "="*60)
    print("WHEN TO USE EACH:")
    print("Direct: simple factual questions ('What is the age of majority?')")
    print("CoT:    multi-step questions requiring legal inference and combining rules")
