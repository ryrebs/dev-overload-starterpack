"""
Week 6 — Evaluate retrieval quality against the golden dataset.

Computes Recall@k and MRR for the indexed legal corpus.

Run golden dataset creation first:
    python 01_golden_dataset.py

Then run this script to measure retrieval quality:
    python 02_retrieval_metrics.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from retrieval import retrieve

GOLDEN_PATH = Path(__file__).parent / "golden.json"


def is_relevant(chunk_source: str, expected_sources: list[str]) -> bool:
    """Check if a retrieved chunk's source matches any expected source."""
    for expected in expected_sources:
        if expected.lower() in chunk_source.lower():
            return True
    return False


def recall_at_k(retrieved_chunks, expected_sources: list[str], k: int) -> float:
    """Fraction of expected sources found in top-k chunks."""
    if not expected_sources:
        return 1.0  # out-of-corpus questions: retrieval not applicable
    found = set()
    for chunk in retrieved_chunks[:k]:
        for expected in expected_sources:
            if expected.lower() in chunk.source.lower():
                found.add(expected)
    return len(found) / len(expected_sources)


def reciprocal_rank(retrieved_chunks, expected_sources: list[str]) -> float:
    """1/position of first relevant result. 0 if no relevant result found."""
    if not expected_sources:
        return 1.0
    for i, chunk in enumerate(retrieved_chunks, 1):
        if is_relevant(chunk.source, expected_sources):
            return 1.0 / i
    return 0.0


def evaluate(k: int = 5):
    if not GOLDEN_PATH.exists():
        print("golden.json not found. Run 01_golden_dataset.py first.")
        return

    golden = json.loads(GOLDEN_PATH.read_text())
    # Filter to questions that have relevant sources (can't measure retrieval for out-of-corpus)
    in_corpus = [q for q in golden if q["expected_established"]]

    print(f"Evaluating retrieval on {len(in_corpus)} in-corpus questions (k={k})...\n")

    recalls = []
    rrs = []
    results = []

    for q in in_corpus:
        chunks = retrieve(q["question"], k=k)
        r = recall_at_k(chunks, q["relevant_sources"], k)
        rr = reciprocal_rank(chunks, q["relevant_sources"])
        recalls.append(r)
        rrs.append(rr)
        results.append({
            "id": q["id"],
            "question": q["question"][:50],
            "recall": r,
            "rr": rr,
            "top_sources": [c.source for c in chunks[:3]],
        })

    print(f"{'ID':<12} {'Question':<52} {'Recall':<8} {'RR':<6} {'Top Sources'}")
    print("-" * 110)
    for r in results:
        print(f"{r['id']:<12} {r['question']:<52} {r['recall']:.2f}    {r['rr']:.2f}   {r['top_sources']}")

    print(f"\n{'='*60}")
    print(f"Recall@{k}:  {sum(recalls)/len(recalls):.3f}  ({sum(recalls)/len(recalls)*100:.1f}%)")
    print(f"MRR:       {sum(rrs)/len(rrs):.3f}")
    print(f"{'='*60}")

    if sum(recalls) / len(recalls) < 0.7:
        print("\nSuggestions to improve recall:")
        print("  - Reduce chunk_size (smaller, more precise chunks)")
        print("  - Try hybrid retrieval (vector + keyword)")
        print("  - Check that all documents are correctly indexed")
    else:
        print("\nRetrieval quality is acceptable. Focus on reasoning quality next.")


if __name__ == "__main__":
    evaluate(k=5)
