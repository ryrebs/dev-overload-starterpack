# Week 3 — Model Formats, Quantization, and Inference Engines

You already ran into this hands-on: F32 models failed, GGUF models worked. This week you understand why, and how to make informed decisions about model selection for any hardware.

---

## The Problem: Models Are Big

A 7B parameter model in full precision (float32) = 7,000,000,000 × 4 bytes = **28 GB**.

Your machine has ~16 GB RAM. A 7B F32 model doesn't fit.

Solution: **quantization** — reduce the precision of each weight.

---

## Number Formats: The Precision Ladder

| Format | Bits | Range | Memory (7B) | Used by |
|--------|------|-------|-------------|---------|
| float32 (F32) | 32 | ~±3.4×10^38 | 28 GB | Training |
| bfloat16 (BF16) | 16 | ~±3.4×10^38 | 14 GB | GPU inference |
| float16 (F16) | 16 | ~±65504 | 14 GB | GPU inference |
| int8 (Q8) | 8 | -128 to 127 | 7 GB | CPU/GPU |
| int4 (Q4) | 4 | -8 to 7 | 3.5 GB | CPU |

BF16 keeps the same exponent range as F32 (important for stability) but halves memory. This is the preferred training format.

For CPU inference: Q4 to Q8. You're trading a tiny quality drop for 4–8× memory reduction.

---

## GGUF: The CPU-Friendly Format

**GGUF** (GPT-Generated Unified Format) is the file format used by `llama.cpp` and Ollama.

What's inside a GGUF file:
- Quantized weight tensors (INT4, INT8, or mixed)
- Model architecture metadata
- Tokenizer vocabulary
- Generation defaults (temperature, context length)

Everything needed to run the model is in one file.

**Naming convention:** `model-name:Q4_K_M`, `model-name:Q8_0`
- `Q4` = 4-bit weights
- `K` = k-quant (smarter quantization that allocates more bits to important weights)
- `M` = medium (a size/quality tradeoff within the quant level)
- `Q8_0` = 8-bit, simpler quantization

**Rule of thumb:** Q4_K_M is the sweet spot for most models — good quality, fits in 4–6 GB. Q8_0 is higher quality but needs 2× memory.

---

## Why F32/BF16 Models Fail on CPU-Only

HuggingFace `.safetensors` files store weights in F32 or BF16. They're designed to be loaded by PyTorch or vLLM, which:
1. Load into GPU VRAM
2. Run CUDA kernels for matrix multiplication

Without a supported GPU, vLLM has no execution path. It fails at startup.

`llama.cpp` (what Ollama uses) is specifically written to run INT4/INT8 operations efficiently on CPU. It uses SIMD instructions (AVX2, NEON) to do quantized matrix multiplies fast on CPU cores.

---

## Inference Engines Compared

| Engine | Formats | Hardware | Best for |
|--------|---------|----------|---------|
| **llama.cpp** | GGUF | CPU, Apple Silicon | Local CPU inference |
| **Ollama** | GGUF (via llama.cpp) | CPU, Apple Silicon | Easy local setup |
| **vLLM** | HF safetensors | GPU (CUDA) | Production GPU serving |
| **HuggingFace Transformers** | HF safetensors | GPU/CPU | Research, fine-tuning |
| **ExLlamaV2** | GGUF, EXL2 | GPU (CUDA) | Fast GPU inference |

**Your setup:** Ollama → llama.cpp → GGUF → CPU. Confirmed working.

---

## Ollama Architecture

```
Your Python code
    → openai.OpenAI(base_url="http://127.0.0.1:11434/v1")
    → Ollama HTTP server (REST API, OpenAI-compatible /v1 endpoint)
    → llama.cpp backend
    → GGUF model weights in RAM
    → CPU matrix multiply (AVX2)
    → tokens → response
```

The OpenAI-compatible endpoint means you can use the `openai` Python library without changing your code when you switch backends (OpenAI, Anthropic, local Ollama).

---

## Performance on CPU

Expect ~5–15 tokens/second on a modern CPU for a 7B Q4 model. Factors:
- **RAM bandwidth** is the bottleneck, not compute. Each token requires loading all weights.
- More CPU cores help, but not linearly.
- Q4 > Q8 in speed (less data to load from RAM).

For legal reasoning with 5 evidence chunks, typical response time: 30–120 seconds. Manageable for offline reasoning, not for live chat.

---

## Choosing a Model for Legal Reasoning

Key considerations:
1. **Domain alignment**: legal-trained models (`saul`, `lexlm`) outperform general models on legal tasks
2. **Instruction-tuned**: must follow the system prompt format
3. **Context length**: must fit `system prompt + 5 chunks (~2k tokens) + question + response`
4. **Quantization**: Q4_K_M or Q8_0 to fit in RAM

`adrienbrault/saul-instruct-v1:Q8_0`: legal domain pretraining + instruction tuning + Q8_0. Best quality option for this project.

---

## Connection to This Project

```python
# config.py
OLLAMA_HOST = "http://127.0.0.1:11434/v1"
LLM_MODEL = "adrienbrault/saul-instruct-v1:Q8_0"
EMBED_MODEL = "bge-m3"
```

Both models are GGUF, served by Ollama, accessed via the OpenAI-compat endpoint. Swapping a model = changing two lines in config.py. The seam is clean.

---

## This Week's Code

1. `01_ollama_api.py` — call Ollama directly, inspect the response format
2. `02_quantization_math.py` — simulate quantizing a float to INT4 and back, measure error
3. `03_model_inspection.py` — inspect GGUF metadata via ollama CLI

```bash
# Requires Ollama running
python 01_ollama_api.py
python 02_quantization_math.py
python 03_model_inspection.py
```
