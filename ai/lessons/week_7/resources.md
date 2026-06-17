# Week 7 Resources

## Must-Read
- **FastAPI official docs** — especially: Path Operations, Request Body, Response Model
- **uvicorn docs** — production deployment settings (workers, timeouts)
- **Pydantic v2 docs** — validators, Field constraints, model_dump()

## Reference
- **FastAPI + Async** — understanding when to use async def vs def
- **Server-Sent Events (SSE)** — how streaming responses work in browsers
- **Docker + FastAPI** — containerizing a Python API

## Practice
- Add a `/batch` endpoint that accepts a list of questions and answers them all
- Add request logging middleware (log question + latency for every request)
- Deploy `02_looyer_api.py` in Docker and test with curl

## What Interviewers Ask
- "How does FastAPI's automatic validation work?"
- "What is ASGI and why does it matter for AI APIs?"
- "How would you handle a 60-second LLM call without timing out the HTTP client?"
- "What is streaming and when would you use it?"
