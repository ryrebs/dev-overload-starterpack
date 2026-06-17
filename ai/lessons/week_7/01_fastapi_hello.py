"""
Week 7 — Minimal FastAPI app. Start here before the full API.

Run: uvicorn 01_fastapi_hello:app --reload
Then visit: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Hello FastAPI",
    description="Minimal example. Foundation for the legal reasoning API.",
    version="0.1.0",
)


# --- Request/Response schemas ---

class EchoRequest(BaseModel):
    message: str
    repeat: int = 1


class EchoResponse(BaseModel):
    original: str
    echoed: str
    word_count: int


# --- Endpoints ---

@app.get("/")
def health():
    """Health check endpoint. Always returns 200 if the server is running."""
    return {"status": "ok", "service": "looyer-api"}


@app.get("/info")
def info():
    """Return API information."""
    return {
        "name": "Looyer Legal API",
        "description": "Local legal reasoning over Philippine law documents",
        "endpoints": ["/", "/info", "/echo", "/query"],
    }


@app.post("/echo", response_model=EchoResponse)
def echo(req: EchoRequest):
    """Echo back a message. Demonstrates request validation and response schema."""
    if req.repeat < 1 or req.repeat > 10:
        raise HTTPException(
            status_code=400,
            detail="repeat must be between 1 and 10",
        )
    echoed = " ".join([req.message] * req.repeat)
    return EchoResponse(
        original=req.message,
        echoed=echoed,
        word_count=len(echoed.split()),
    )


# Try sending invalid data to see automatic validation:
# curl -X POST http://localhost:8000/echo -H "Content-Type: application/json" -d '{"repeat": "not a number"}'
# FastAPI returns 422 with a clear error — no validation code written.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("01_fastapi_hello:app", host="0.0.0.0", port=8000, reload=True)
