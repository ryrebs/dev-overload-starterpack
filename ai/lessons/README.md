# AI Engineering Crash Course

A self-contained curriculum for going from fundamentals to hireable AI engineer.
Built alongside a real project: a legal document reasoning system using local LLMs,
vector search, and structured retrieval.

---

## Who this is for

You are:
- Building a local RAG system (document reasoning with LLMs)
- Learning AI engineering with the goal of getting hired
- Comfortable with Python
- Working on Linux, CPU-only hardware

---

## How to use this

Each week is a folder. Inside every folder:
- `README.md` — theory, concepts, vocabulary. **Read this first.**
- Python files — runnable examples. **Run these after reading.**
- `resources.md` — official docs, papers, videos. Go deeper here.

**Do not skip the code.** Reading theory without running it is 30% as effective.
**Do not skip the theory.** Running code without understanding is copy-paste engineering.

---

## Prerequisites

- Python 3.11
- Basic Python: functions, classes, lists, dicts
- Basic command line
- Ollama installed and running

Install base deps for the course:
```bash
pip install numpy matplotlib torch transformers openai anthropic chromadb \
            llama-index-core sentence-transformers ragas fastapi uvicorn \
            pydantic instructor datasets peft accelerate bitsandbytes
```

---

## Timeline

| | Week | Topics | Notes |
|---|------|--------|-------|
| **Part 1** | Week 1 | Neural networks, weights, training, backprop | Pure theory + numpy |
| | Week 2 | LLMs, transformers, attention, tokens, context | Core of everything |
| **Part 2** | Week 3 | Model formats, quantization, inference engines | You've experienced this |
| | Week 4 | Embeddings, vector search, RAG | You've built this |
| **Part 3** | Week 5 | Prompt engineering | High-leverage skill |
| | Week 6 | Evaluation and benchmarking | What separates engineers from hobbyists |
| | Week 7 | FastAPI deployment | Build a real API around your pipeline |
| | Week 8 | Agents, tool use, LlamaIndex orchestration | Where the field is going |
| **Part 4** | Week 9 | Fine-tuning, LoRA, QLoRA | Requires GPU (Colab works) |

> **Weeks 3 & 4** — you've already touched these by building the project.
> Still read them. The goal is to formalize the mental models, not repeat the work.

---

## Curriculum

### Part 1 — Foundations (Weeks 1–2)
How neural networks learn. What weights actually store. How the Transformer
architecture works. This is the theory everything else builds on. Do not skip it.

### Part 2 — Models & Engines (Weeks 3–4)
How models are stored, quantized, and executed. How embeddings encode meaning.
How RAG pipelines connect retrieval to generation. You've done this in practice —
now understand it deeply enough to explain it and make better decisions.

### Part 3 — Applied Engineering (Weeks 5–8)
Prompt engineering, evaluation, FastAPI deployment, and agents. These are the practical
skills employers test in interviews. **LlamaIndex** is the AI framework used throughout
for retrieval and orchestration. **FastAPI** is used for deployment (Week 7). Agent
architectures (ReAct, Plan-and-Execute, multi-agent) are covered in Week 8.

### Part 4 — Advanced (Month 3)
Fine-tuning a model on your own data using LoRA/QLoRA. Requires GPU access.
Google Colab (free tier) is enough to complete this section.

---

## The Project as Your Portfolio

The legal reasoning system you are building IS your portfolio piece. Every week,
connect what you learn back to it:

- Week 1–2 → understand WHY bge-m3 produces embeddings
- Week 3–4 → understand WHY GGUF runs on CPU and F32 does not
- Week 5 → improve the reasoning prompt in `reasoning.py`
- Week 6 → build the golden eval set
- Week 7 → wrap the system in a FastAPI endpoint
- Week 8 → add the retrieve→reason→re-retrieve loop
- Month 3 → fine-tune a small model on Philippine legal QA data

**One rule: build while you learn.**

---

## Key Vocabulary (master these before interviews)

| Term | One-line definition |
|------|---------------------|
| Parameter / Weight | A number the model learned during training |
| Token | The smallest unit of text the model processes |
| Embedding | A vector (list of numbers) that represents meaning |
| Transformer | The neural network architecture all modern LLMs use |
| Attention | The mechanism that lets the model relate words to each other |
| Context window | How much text the model can "see" at once |
| Inference | Running a trained model to get output (vs training) |
| Quantization | Reducing weight precision to save memory and speed up CPU |
| GGUF | File format for quantized models (llama.cpp / Ollama) |
| RAG | Retrieval-Augmented Generation — answer from retrieved docs |
| Fine-tuning | Further training a pretrained model on new data |
| LoRA | Low-Rank Adaptation — efficient fine-tuning technique |
| Agent | An LLM that can use tools and loop until a goal is met |
| Prompt engineering | Designing inputs to get better outputs from LLMs |

---

## Confidence check before interviews

You should be able to answer these from memory:

1. What does a weight represent, and what changes it during training?
2. How does the attention mechanism decide which words to focus on?
3. Why can't you run an F32 model efficiently on CPU?
4. What does bge-m3 actually return when you call `embed_texts()`?
5. What's the difference between RAG and fine-tuning for domain knowledge?
6. What does `established=False` mean in this project's reasoning output?
7. How would you evaluate whether your retrieval is actually working?
8. What is LoRA and why is it better than full fine-tuning on limited hardware?
