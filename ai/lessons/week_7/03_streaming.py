"""
Week 7 — Streaming responses with FastAPI.

Users see tokens as they arrive instead of waiting for the full response.
Run: uvicorn 03_streaming:app --reload
Test: curl -N http://localhost:8000/stream?question=What+is+habeas+corpus
"""

import sys
import json
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import OpenAI

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config import OLLAMA_HOST, LLM_MODEL
from retrieval import retrieve, EvidenceChunk

app = FastAPI(title="Looyer Streaming API")

client = OpenAI(base_url=OLLAMA_HOST, api_key="ollama")


def build_evidence_block(chunks: list[EvidenceChunk]) -> str:
    return "\n\n".join(f"[{i+1}] Source: {c.source}\n{c.text}" for i, c in enumerate(chunks))


async def stream_answer(question: str, k: int = 5) -> AsyncGenerator[str, None]:
    """Generator that yields Server-Sent Events (SSE) tokens."""
    chunks = retrieve(question, k=k)
    evidence = build_evidence_block(chunks)

    messages = [
        {
            "role": "system",
            "content": "You are a Philippine legal assistant. Base your answer strictly on the evidence.",
        },
        {
            "role": "user",
            "content": f"EVIDENCE:\n{evidence}\n\nQUESTION: {question}",
        },
    ]

    # Ollama streaming via openai client
    stream = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        max_tokens=500,
        temperature=0.1,
        stream=True,
    )

    for chunk in stream:
        token = chunk.choices[0].delta.content
        if token:
            # SSE format: data: {json}\n\n
            yield f"data: {json.dumps({'token': token})}\n\n"

    yield f"data: {json.dumps({'done': True})}\n\n"


@app.get("/stream")
async def stream_query(question: str, k: int = 5):
    """
    Stream a legal answer token by token.
    Frontend reads tokens as they arrive (much better perceived latency).
    """
    return StreamingResponse(
        stream_answer(question, k=k),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


# JavaScript client example (for a frontend):
# const evtSource = new EventSource('/stream?question=What+is+habeas+corpus');
# evtSource.onmessage = (e) => {
#     const data = JSON.parse(e.data);
#     if (data.done) evtSource.close();
#     else document.getElementById('answer').textContent += data.token;
# };


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("03_streaming:app", host="0.0.0.0", port=8000, reload=True)
