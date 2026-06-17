"""
Week 6 — Build and save a golden evaluation dataset for the legal reasoning system.

Run this once to create golden.json. Then use 02_retrieval_metrics.py to evaluate.
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

GOLDEN_PATH = Path(__file__).parent / "golden.json"

# Hand-crafted golden questions for the Philippine legal corpus
# These are questions whose answers CAN be verified against the indexed documents.
GOLDEN_DATASET = [
    {
        "id": "const_001",
        "question": "What rights does an accused person have under the Philippine Constitution?",
        "relevant_sources": ["constitution.md"],
        "expected_established": True,
        "expected_keywords": ["presumed innocent", "counsel", "due process", "Section 14"],
        "notes": "Article III Section 14 — criminal rights",
    },
    {
        "id": "const_002",
        "question": "Is warrantless arrest allowed? Under what circumstances?",
        "relevant_sources": ["constitution.md"],
        "expected_established": True,
        "expected_keywords": ["warrant", "arrest", "Section 2"],
        "notes": "Article III Section 2 — search and seizure",
    },
    {
        "id": "const_003",
        "question": "What does the Philippine Constitution say about freedom of speech?",
        "relevant_sources": ["constitution.md"],
        "expected_established": True,
        "expected_keywords": ["expression", "speech", "press", "Section 4"],
        "notes": "Article III Section 4 — freedom of expression",
    },
    {
        "id": "civil_001",
        "question": "At what age does a person reach the age of majority in the Philippines?",
        "relevant_sources": ["civil_code.md"],
        "expected_established": True,
        "expected_keywords": ["18", "eighteen", "majority", "Article 234"],
        "notes": "Civil Code Article 234 — emancipation and majority",
    },
    {
        "id": "civil_002",
        "question": "What are the essential elements of a valid contract?",
        "relevant_sources": ["civil_code.md"],
        "expected_established": True,
        "expected_keywords": ["consent", "object", "cause", "Article 1318"],
        "notes": "Civil Code Article 1318 — requisites of a contract",
    },
    {
        "id": "civil_003",
        "question": "Can a minor enter into a contract? What is the legal effect?",
        "relevant_sources": ["civil_code.md"],
        "expected_established": True,
        "expected_keywords": ["minor", "voidable", "Article 1327"],
        "notes": "Civil Code Article 1327 — incapacity to contract",
    },
    {
        "id": "civil_004",
        "question": "How is property ownership transferred under Philippine law?",
        "relevant_sources": ["civil_code.md"],
        "expected_established": True,
        "expected_keywords": ["succession", "donation", "contract", "Article 712"],
        "notes": "Civil Code Article 712 — modes of acquiring ownership",
    },
    {
        "id": "out_001",
        "question": "What is the corporate income tax rate in the Philippines?",
        "relevant_sources": [],
        "expected_established": False,
        "expected_keywords": [],
        "notes": "Tax law — not in the indexed corpus",
    },
    {
        "id": "out_002",
        "question": "What is the penalty for jaywalking?",
        "relevant_sources": [],
        "expected_established": False,
        "expected_keywords": [],
        "notes": "Local ordinance — not in the indexed corpus",
    },
    {
        "id": "cross_001",
        "question": "Can an 18-year-old enter into a valid contract?",
        "relevant_sources": ["civil_code.md"],
        "expected_established": True,
        "expected_keywords": ["majority", "18", "consent", "capacity"],
        "notes": "Requires combining age of majority + contract capacity",
    },
]


def save_golden_dataset():
    GOLDEN_PATH.write_text(json.dumps(GOLDEN_DATASET, indent=2))
    print(f"Saved {len(GOLDEN_DATASET)} golden questions to {GOLDEN_PATH}")
    print("\nBreakdown:")
    by_source = {}
    for q in GOLDEN_DATASET:
        key = ",".join(q["relevant_sources"]) or "out-of-corpus"
        by_source[key] = by_source.get(key, 0) + 1
    for source, count in sorted(by_source.items()):
        print(f"  {source}: {count} questions")

    out_of_scope = sum(1 for q in GOLDEN_DATASET if not q["expected_established"])
    print(f"\n  expected_established=True:  {len(GOLDEN_DATASET) - out_of_scope}")
    print(f"  expected_established=False: {out_of_scope}")


if __name__ == "__main__":
    save_golden_dataset()
    print("\nNext: run 02_retrieval_metrics.py to evaluate retrieval quality.")
