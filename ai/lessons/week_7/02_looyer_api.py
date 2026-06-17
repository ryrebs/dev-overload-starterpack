"""
Week 7 — Full legal reasoning API.

Wraps the retrieve + reason pipeline in FastAPI endpoints.

Run: uvicorn 02_looyer_api:app --reload
Test: curl -X POST http://localhost:8000/query \
         -H "Content-Type: application/json" \
         -d '{"question": "What are the rights of an accused?"}'
"""

import sys
import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Add project root to path so we can import the pipeline
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from retrieval import retrieve
from reasoning import reason

app = FastAPI(
    title="Looyer — Philippine Legal Reasoning API",
    description="Retrieval-augmented legal reasoning over the 1987 Constitution and Civil Code.",
    version="1.0.0",
)

# CORS: allow browser clients (remove or restrict origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# --- Schemas ---

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5, description="Legal question to answer")
    k: int = Field(default=5, ge=1, le=20, description="Number of evidence chunks to retrieve")


class CitationOut(BaseModel):
    source: str
    quote: str


class QueryResponse(BaseModel):
    question: str
    established: bool
    answer: str
    citations: list[CitationOut]
    chunks_retrieved: int
    latency_ms: int


# --- Endpoints ---

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    """
    Answer a legal question using the indexed Philippine legal corpus.

    Returns:
    - established=True: answer derived from evidence, with citations
    - established=False: evidence insufficient; answer contains legal inference
    """
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    start = time.time()
    try:
        chunks = retrieve(req.question, k=req.k)
        result = reason(req.question, chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")

    latency_ms = int((time.time() - start) * 1000)

    return QueryResponse(
        question=req.question,
        established=result.established,
        answer=result.answer,
        citations=[CitationOut(source=c.source, quote=c.quote) for c in result.citations],
        chunks_retrieved=len(chunks),
        latency_ms=latency_ms,
    )


@app.get("/status")
def status():
    """Return pipeline status and model configuration."""
    from config import LLM_MODEL, EMBED_MODEL, OLLAMA_HOST
    return {
        "llm_model": LLM_MODEL,
        "embed_model": EMBED_MODEL,
        "ollama_host": OLLAMA_HOST,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("02_looyer_api:app", host="0.0.0.0", port=8000, reload=True)
