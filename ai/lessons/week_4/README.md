# Week 4 — Embeddings, Vector Search, and RAG

You've built this in the project. This week formalizes the mental model so you can explain it, optimize it, and debug it.

---

## What an Embedding Is

An embedding is a function that maps text to a vector in a high-dimensional space, such that **semantically similar texts are geometrically close**.

```
embed("rights of the accused") → [0.23, -0.11, 0.87, ..., 0.04]  # 1024 numbers
embed("due process rights")    → [0.21, -0.09, 0.84, ..., 0.06]  # close in space
embed("recipe for pasta")      → [-0.54, 0.33, -0.12, ..., 0.71] # far in space
```

The 1024 dimensions are not interpretable individually. The *distance* between vectors is what carries meaning.

---

## How Similarity Is Measured

**Cosine similarity**: measures the angle between two vectors (ignores magnitude, only direction).

```
cos(A, B) = (A · B) / (|A| × |B|)
```

Range: -1 (opposite) to 1 (identical direction).

**Why cosine for text embeddings**: two passages can have different lengths (different magnitudes) but express the same idea. Cosine correctly scores them as similar; Euclidean distance would not.

---

## bge-m3: Your Embedding Model

**BGE-M3** (BAAI General Embedding, Multi-Lingual, Multi-Granularity, Multi-Functionality) is a 568M parameter transformer fine-tuned to produce semantic embeddings.

Key properties:
- 1024-dimensional output vectors
- Works across 100+ languages (Filipino legal content will work)
- Supports dense (cosine), sparse (BM25-like), and colbert-style retrieval
- Pulled via Ollama, runs on CPU

When you call `embed_texts(["Article 1..."])`:
1. Text → tokenizer → token IDs
2. Token IDs → transformer (568M parameters)
3. Mean pooling of last hidden states (or `[CLS]` token)
4. L2 normalization → unit vector
5. Return 1024-dimensional vector

---

## Chroma: The Vector Database

Chroma is an embedded vector database (no server needed — runs in your process).

It stores:
- The embedding vectors
- The original text (document)
- Metadata (source filename, chunk index, etc.)

At query time:
1. Embed the query text
2. Compute cosine similarity between query vector and all stored vectors
3. Return top-k most similar documents

For cosine similarity, Chroma normalizes vectors and uses inner product (which equals cosine similarity for unit vectors).

---

## Chunking: Why It Matters

You can't embed an entire document as one vector — you'd lose precision. A 50-page document as one vector averages out all its content into a blob that matches nothing specifically.

Chunking splits documents into smaller pieces before embedding. Each chunk gets its own vector.

**Trade-off:**
- Chunks too large → imprecise, match too broadly
- Chunks too small → lose context, a sentence without its section heading is ambiguous

**LlamaIndex MarkdownNodeParser + SentenceSplitter** (what you use):
1. `MarkdownNodeParser`: splits on headings `#`, `##`, `###` — keeps section context
2. `SentenceSplitter(chunk_size=512, chunk_overlap=50)`: further splits long sections, overlapping edges to avoid cutting context

Result: each chunk is a coherent, bounded piece of text with its section heading preserved.

---

## RAG: Retrieval-Augmented Generation

Standard LLM: question → LLM → answer (uses model's training data, may hallucinate)

RAG:
1. question → embedding model → query vector
2. query vector → vector DB → top-k relevant chunks
3. question + chunks → LLM → grounded answer

**Why RAG for legal reasoning:**
- LLMs don't know the 1987 Philippine Constitution verbatim
- Even if they did, they can't cite specific provisions reliably
- RAG forces the answer to come from actual retrieved text
- You control the source; you can verify citations

---

## The Retrieval Seam in This Project

```python
# retrieval.py
def retrieve(question: str, k: int = 5) -> list[EvidenceChunk]:
    retriever = _load_retriever(k)
    nodes = retriever.retrieve(question)
    return [EvidenceChunk(text, source, score, metadata) for node in nodes]
```

This is **Layer 4** — it only retrieves. It doesn't interpret. The reasoning is Layer 5.

`EvidenceChunk` is a plain dataclass. The retriever doesn't know what happens to the chunks after it returns them. This is the seam: you can swap out the retriever without touching the reasoning layer.

---

## LlamaIndex as Retriever (Not Query Engine)

LlamaIndex can be used end-to-end (it will retrieve AND generate). We don't use it that way.

We use only: `VectorStoreIndex.as_retriever(similarity_top_k=k)`

This gives us:
- Embedding of the query via our `_DMREmbedding` adapter
- Chroma lookup
- `NodeWithScore` objects back

The reason not to use `as_query_engine()`:
- It would call the LLM internally, bypassing our system prompt and citation schema
- We lose control of the retrieve/reason boundary
- `instructor` structured output wouldn't be applied

**LlamaIndex is used as retrieval infrastructure, not as the reasoning brain.**

---

## Hybrid Retrieval (Future)

Pure vector search has a weakness: it misses exact keyword matches. "Article 3 Section 4" has a specific vector that might not match a question asking about it by number.

**Hybrid retrieval** combines:
- Dense (vector): semantic similarity
- Sparse (BM25/keyword): exact term matching

LlamaIndex supports this. When you want better recall on specific legal article references, this is the upgrade path. Architecture seam is already in place.

---

## Connection to This Project

```
Civil Code PDF → pymupdf4llm → Markdown
                              ↓
                    MarkdownNodeParser
                              ↓
                    SentenceSplitter (512 tokens)
                              ↓
                    embed_texts() → bge-m3 → 1024-dim vectors
                              ↓
                    Chroma persistent collection "looyer"
                              ↓ (query time)
                    retrieve("What are the rights of accused?")
                              ↓
                    top-5 EvidenceChunks → reason()
```

---

## This Week's Code

1. `01_embeddings_demo.py` — visualize cosine similarity between text pairs
2. `02_chroma_basics.py` — create a mini Chroma collection, insert, query
3. `03_simple_rag.py` — minimal end-to-end RAG: embed text → store → retrieve → answer

```bash
pip install chromadb openai sentence-transformers
python 01_embeddings_demo.py
python 02_chroma_basics.py
python 03_simple_rag.py
```
