"""
Week 8 — The retrieve → reason → re-retrieve loop.

When established=False, the model tells us what's missing.
We use that information to do a refined second search.

This is the core reasoning loop for the legal system.
"""

import sys
from pathlib import Path
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from retrieval import retrieve, EvidenceChunk
from reasoning import reason, ReasoningResult


def deduplicate_chunks(chunks: list[EvidenceChunk]) -> list[EvidenceChunk]:
    """Remove duplicate chunks by text content."""
    seen = set()
    unique = []
    for c in chunks:
        key = c.text[:100]  # first 100 chars as fingerprint
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique


def extract_search_hint(result: ReasoningResult, original_question: str) -> str:
    """
    When established=False, extract a refined search query from the answer.
    The model explains what's missing — use that as the next search.
    """
    if result.answer:
        # The answer often says "I need information about X" or "The provision on Y is missing"
        # Combine original question with the missing info hint
        return f"{original_question}\n{result.answer[:200]}"
    return original_question


@dataclass
class LoopResult:
    final_result: ReasoningResult
    attempts: int
    total_chunks: int
    refinements_used: list[str]


def query_with_loop(
    question: str,
    k: int = 5,
    max_attempts: int = 3,
    verbose: bool = True,
) -> LoopResult:
    """
    Retrieve → reason → if not established, refine and retry.

    Args:
        question:     the user's legal question
        k:            chunks per retrieval attempt
        max_attempts: max re-retrieve iterations
        verbose:      print progress

    Returns:
        LoopResult with final answer and diagnostics
    """
    all_chunks: list[EvidenceChunk] = []
    refinements = []

    current_query = question

    for attempt in range(1, max_attempts + 1):
        if verbose:
            print(f"\n[Attempt {attempt}/{max_attempts}]")
            print(f"  Query: '{current_query[:80]}...'")

        # Retrieve
        new_chunks = retrieve(current_query, k=k)
        all_chunks = deduplicate_chunks(all_chunks + new_chunks)

        if verbose:
            print(f"  Chunks: {len(new_chunks)} new, {len(all_chunks)} total (deduplicated)")

        # Reason
        result = reason(question, all_chunks)

        if verbose:
            print(f"  Established: {result.established}")

        if result.established:
            if verbose:
                print(f"  Answer found on attempt {attempt}.")
            return LoopResult(
                final_result=result,
                attempts=attempt,
                total_chunks=len(all_chunks),
                refinements_used=refinements,
            )

        if attempt < max_attempts:
            # Refine the query using what the model said was missing
            refined_query = extract_search_hint(result, question)
            if refined_query != current_query:
                refinements.append(refined_query)
                current_query = refined_query
                if verbose:
                    print(f"  Refined query: '{refined_query[:80]}...'")
            else:
                if verbose:
                    print("  Could not refine query further. Stopping.")
                break

    # Return the best result we have, even if not established
    return LoopResult(
        final_result=result,
        attempts=attempt,
        total_chunks=len(all_chunks),
        refinements_used=refinements,
    )


if __name__ == "__main__":
    print("=== Retrieve → Reason → Re-retrieve Loop ===\n")

    test_questions = [
        "What are the rights of an accused person under Philippine law?",
        "Can a minor enter into a binding contract?",
        "What is the maximum penalty for theft in the Philippines?",  # likely not in corpus
    ]

    for question in test_questions:
        print(f"\n{'='*60}")
        print(f"QUESTION: {question}")
        print(f"{'='*60}")

        loop_result = query_with_loop(question, k=5, max_attempts=2, verbose=True)
        result = loop_result.final_result

        print(f"\nFINAL RESULT:")
        print(f"  Established:  {result.established}")
        print(f"  Attempts:     {loop_result.attempts}")
        print(f"  Total chunks: {loop_result.total_chunks}")
        print(f"  Answer: {result.answer[:300]}...")
        if result.citations:
            print(f"  Citations: {len(result.citations)}")
            for c in result.citations[:2]:
                print(f"    [{c.source}] {c.quote[:80]}...")
