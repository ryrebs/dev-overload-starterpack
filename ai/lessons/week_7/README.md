# Week 7 — FastAPI: Wrapping AI Systems for Deployment

You have a working legal reasoning pipeline. This week you turn it into a service that anything can call — a web app, a mobile client, a CLI, another service.

FastAPI is the right choice: it's async-first, has automatic OpenAPI docs, validates inputs with Pydantic (which you already know), and is the industry standard for Python AI APIs.

---

## Why FastAPI

| | Flask | FastAPI | Django REST |
|---|-------|---------|------------|
| Speed | Sync | Async (ASGI) | Sync |
| Type hints | Optional | Native | Optional |
| Validation | Manual | Auto (Pydantic) | Serializers |
| OpenAPI docs | Plugin | Built-in | drf-spectacular |
| AI workload fit | OK | Best | Overkill |

FastAPI's automatic validation matters for AI APIs: you get request schema enforcement and response schema documentation for free, using the same Pydantic models you already use for LLM output.

---

## The Simplest Possible FastAPI App

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}
```

Run it:
```bash
uvicorn main:app --reload
```

Uvicorn is the ASGI server. `--reload` restarts on code changes. Visit `http://localhost:8000/docs` for the automatic OpenAPI UI.

---

## Async: Why It Matters for LLM APIs

LLM inference is slow (5–60 seconds). If your server is synchronous:

```
Request 1 arrives → process 60s → respond
Request 2 arrives → BLOCKED for 60s waiting for request 1 to finish
```

With async:
```
Request 1 arrives → start LLM call → yield control
Request 2 arrives → start LLM call → yield control
Request 1 LLM done → respond
Request 2 LLM done → respond
```

Both requests are processing simultaneously. Response time is max(R1, R2), not R1 + R2.

Use `async def` for route handlers. Use `await` for I/O operations (LLM calls, DB reads).

---

## Wrapping the Legal Reasoning Pipeline

```python
from fastapi import FastAPI
from pydantic import BaseModel
from retrieval import retrieve
from reasoning import reason, ReasoningResult

app = FastAPI(title="Looyer — Legal Reasoning API")

class QueryRequest(BaseModel):
    question: str
    k: int = 5  # number of evidence chunks

class QueryResponse(BaseModel):
    established: bool
    answer: str
    citations: list[dict]
    chunks_used: int

@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    chunks = retrieve(req.question, k=req.k)
    result = reason(req.question, chunks)
    return QueryResponse(
        established=result.established,
        answer=result.answer,
        citations=[{"source": c.source, "quote": c.quote} for c in result.citations],
        chunks_used=len(chunks),
    )
```

Now anyone can `POST /query` with `{"question": "..."}` and get a structured legal answer.

---

## Request Validation (Free from Pydantic)

```python
class QueryRequest(BaseModel):
    question: str         # required, must be string
    k: int = 5            # optional, defaults to 5
    max_tokens: int = 512 # optional
```

If someone sends `{"question": 123}` — FastAPI returns a 422 with a clear error. No validation code written.

---

## Streaming Responses

LLMs generate one token at a time. For long answers, you want to stream rather than wait for the full response.

```python
from fastapi.responses import StreamingResponse

@app.post("/query/stream")
async def query_stream(req: QueryRequest):
    async def generate():
        chunks = retrieve(req.question, k=req.k)
        # streaming via Ollama's streaming API
        for token in stream_reason(req.question, chunks):
            yield f"data: {token}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
```

The client receives tokens as they arrive. Perceived latency drops significantly.

---

## Error Handling

```python
from fastapi import HTTPException

@app.post("/query")
async def query(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    try:
        chunks = retrieve(req.question, k=req.k)
        result = reason(req.question, chunks)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

Return specific HTTP status codes. 400 for bad input. 500 for server errors. 422 is automatic for schema violations.

---

## Background Tasks

For expensive operations you don't want in the request path:

```python
from fastapi import BackgroundTasks

@app.post("/ingest")
async def ingest_document(file_path: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_ingestion_pipeline, file_path)
    return {"status": "ingestion started"}
```

The `/ingest` endpoint returns immediately. Ingestion runs in the background. The client can poll a status endpoint.

---

## CORS (Cross-Origin Resource Sharing)

If a browser-based frontend calls your API:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your frontend URL
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
```

Without this, browsers block cross-origin requests. Your CLI client doesn't need this — only browsers do.

---

## OpenAPI Docs (Free)

Visit `http://localhost:8000/docs` after starting the server:
- Interactive API documentation
- Try out all endpoints in the browser
- Automatically generated from your type hints and docstrings

This is your API's built-in user manual. No extra work required.

---

## Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system
COPY . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t looyer .
docker run -p 8000:8000 -e OLLAMA_HOST=http://host.docker.internal:11434/v1 looyer
```

The Ollama instance runs on the host; the FastAPI app connects to it via `host.docker.internal`.

---

## Connection to This Project

Layer 7 in the architecture is "Orchestration." FastAPI is the outer shell that:
1. Accepts HTTP requests
2. Calls `retrieve()` (Layer 4)
3. Calls `reason()` (Layer 5)
4. Returns structured JSON responses

The pipeline logic stays in `retrieval.py` and `reasoning.py`. `api.py` is purely a thin HTTP wrapper.

---

## This Week's Code

1. `01_fastapi_hello.py` — minimal FastAPI app with health and echo endpoints
2. `02_looyer_api.py` — full legal reasoning API wrapping the pipeline
3. `03_streaming.py` — streaming response endpoint
4. `04_background_tasks.py` — async document ingestion endpoint

```bash
pip install fastapi uvicorn
uvicorn 01_fastapi_hello:app --reload
uvicorn 02_looyer_api:app --reload
```
