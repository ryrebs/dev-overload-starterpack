"""
Week 9 — Prepare a fine-tuning dataset from the legal documents.

Reads the indexed documents and generates Q&A pairs for fine-tuning.
Output: training_data.jsonl (sharegpt format)
"""

import json
import sys
from pathlib import Path
from openai import OpenAI

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")
LLM_MODEL = "adrienbrault/saul-instruct-v1:Q8_0"
OUTPUT_PATH = Path(__file__).parent / "training_data.jsonl"


def generate_qa_pair(passage: str, source: str) -> dict | None:
    """
    Given a passage, ask an LLM to generate a realistic Q&A pair.
    Returns a ShareGPT-format training example.
    """
    prompt = f"""Given this legal passage from {source}:

---
{passage}
---

Generate ONE realistic question that could be asked about this passage, and a concise answer.
Respond in JSON:
{{"question": "...", "answer": "..."}}

The answer should cite the specific provision and be 2-4 sentences."""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.3,
    )

    text = response.choices[0].message.content.strip()
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        data = json.loads(text[start:end])
        question = data.get("question", "").strip()
        answer = data.get("answer", "").strip()
        if not question or not answer:
            return None

        # ShareGPT format
        return {
            "conversations": [
                {"from": "system", "value": "You are a Philippine legal assistant. Cite specific articles and provisions."},
                {"from": "human", "value": question},
                {"from": "gpt", "value": answer},
            ]
        }
    except (json.JSONDecodeError, KeyError):
        return None


# Sample passages (in production, these come from the parsed documents)
SAMPLE_PASSAGES = [
    {
        "text": "Section 14. (1) No person shall be held to answer for a criminal offense without due process of law. (2) In all criminal prosecutions, the accused shall be presumed innocent until the contrary is proved, and shall enjoy the right to be heard by himself and counsel, to be informed of the nature and cause of the accusation against him, to have a speedy, impartial, and public trial, to meet the witnesses face to face, and to have compulsory process to secure the attendance of witnesses and the production of evidence in his behalf.",
        "source": "1987 Philippine Constitution, Article III",
    },
    {
        "text": "Article 234. Emancipation takes place by the attainment of majority. Unless otherwise provided, majority commences at the age of eighteen years. Marriage shall not be required for emancipation.",
        "source": "Civil Code of the Philippines",
    },
    {
        "text": "Article 1318. There is no contract unless the following requisites concur: (1) Consent of the contracting parties; (2) Object certain which is the subject matter of the contract; (3) Cause of the obligation which is established.",
        "source": "Civil Code of the Philippines",
    },
    {
        "text": "Article 1327. The following cannot give consent to a contract: (1) Unemancipated minors; (2) Insane or demented persons, and deaf-mutes who do not know how to write.",
        "source": "Civil Code of the Philippines",
    },
    {
        "text": "Article 712. Ownership is acquired by occupation and by intellectual creation. Ownership and other real rights over property are acquired and transmitted by law, by donation, by testate and intestate succession, and in consequence of certain contracts, by tradition.",
        "source": "Civil Code of the Philippines",
    },
]


def build_training_set(passages: list[dict], verbose: bool = True) -> list[dict]:
    examples = []
    for i, passage in enumerate(passages):
        if verbose:
            print(f"Generating Q&A for passage {i+1}/{len(passages)}: {passage['text'][:60]}...")
        example = generate_qa_pair(passage["text"], passage["source"])
        if example:
            examples.append(example)
            if verbose:
                q = example["conversations"][1]["value"]
                a = example["conversations"][2]["value"]
                print(f"  Q: {q[:80]}...")
                print(f"  A: {a[:80]}...")
        else:
            if verbose:
                print(f"  Failed to generate Q&A for this passage.")

    return examples


if __name__ == "__main__":
    print("=== Building Fine-Tuning Dataset ===\n")
    print("This generates Q&A pairs from legal passages using the LLM.")
    print("In production, use all chunks from your indexed corpus.\n")

    examples = build_training_set(SAMPLE_PASSAGES)

    # Save as JSONL
    with OUTPUT_PATH.open("w") as f:
        for ex in examples:
            f.write(json.dumps(ex) + "\n")

    print(f"\nSaved {len(examples)} training examples to {OUTPUT_PATH}")
    print(f"\nFirst example:")
    if examples:
        print(json.dumps(examples[0], indent=2))
    print(f"\nNext: use 03_qlora_training.py in Google Colab to fine-tune a model on this data.")
