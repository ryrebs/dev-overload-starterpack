"""
Week 8 — LlamaIndex QueryPipeline: deterministic chain for the legal reasoning system.

This is Layer 7 of the architecture. The pipeline wires:
  input → retriever → reasoner → output

QueryPipeline gives us: logging, component swapping, and a clean architecture.
"""

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from llama_index.core.query_pipeline import QueryPipeline, InputComponent, CustomQueryComponent
from llama_index.core.schema import QueryBundle
from pydantic import BaseModel

from retrieval import retrieve, EvidenceChunk
from reasoning import reason, ReasoningResult


class RetrieverComponent(CustomQueryComponent):
    """Wraps our retrieve() function as a LlamaIndex pipeline component."""

    k: int = 5

    @property
    def _input_keys(self) -> set:
        return {"question"}

    @property
    def _output_keys(self) -> set:
        return {"question", "chunks"}

    def _run_component(self, **kwargs: Any) -> dict:
        question = kwargs["question"]
        chunks = retrieve(question, k=self.k)
        print(f"  [Retriever] Found {len(chunks)} chunks for: '{question[:50]}...'")
        return {"question": question, "chunks": chunks}


class ReasonerComponent(CustomQueryComponent):
    """Wraps our reason() function as a LlamaIndex pipeline component."""

    @property
    def _input_keys(self) -> set:
        return {"question", "chunks"}

    @property
    def _output_keys(self) -> set:
        return {"result"}

    def _run_component(self, **kwargs: Any) -> dict:
        question = kwargs["question"]
        chunks = kwargs["chunks"]
        print(f"  [Reasoner] Reasoning over {len(chunks)} chunks...")
        result = reason(question, chunks)
        return {"result": result}


def build_pipeline(k: int = 5) -> QueryPipeline:
    """Assemble the retrieval → reasoning pipeline."""
    pipeline = QueryPipeline(verbose=False)

    pipeline.add_modules({
        "input": InputComponent(),
        "retriever": RetrieverComponent(k=k),
        "reasoner": ReasonerComponent(),
    })

    # Wire the modules together
    pipeline.add_link("input", "retriever", src_key="question", dest_key="question")
    pipeline.add_link("retriever", "reasoner", src_key="question", dest_key="question")
    pipeline.add_link("retriever", "reasoner", src_key="chunks", dest_key="chunks")

    return pipeline


def run_query(pipeline: QueryPipeline, question: str) -> ReasoningResult:
    print(f"\nQuery: {question}")
    output = pipeline.run(question=question)
    return output["result"]


if __name__ == "__main__":
    print("=== LlamaIndex QueryPipeline: Legal Reasoning ===\n")
    print("Building pipeline...")
    pipeline = build_pipeline(k=5)
    print("Pipeline ready.\n")

    questions = [
        "What are the rights of an accused person?",
        "At what age does a person reach majority?",
    ]

    for q in questions:
        result = run_query(pipeline, q)
        print(f"\nEstablished: {result.established}")
        print(f"Answer: {result.answer[:200]}...")
        if result.citations:
            print(f"Citations: {[c.source for c in result.citations]}")
        print()
