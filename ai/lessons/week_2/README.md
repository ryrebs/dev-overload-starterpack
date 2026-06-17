# Week 2 — LLMs and the Transformer Architecture

Every language model you will use — GPT, LLaMA, Mistral, Qwen, the Saul legal model — is a Transformer. This week you understand what that means at a level that lets you make engineering decisions.

---

## The Core Problem: Understanding Context

Old models (RNNs) processed text left-to-right, one token at a time. By the time they reached word 100, they'd "forgotten" word 1.

Transformers solve this: **every token attends to every other token simultaneously**. The model can relate "accused" at position 87 directly to "rights" at position 3, with no forgetting.

---

## Tokens: What the Model Actually Sees

LLMs don't see characters or words — they see **tokens**.

A tokenizer splits text into pieces. Common strategy: Byte-Pair Encoding (BPE).

```
"Constitution" → ["Constit", "ution"]       # 2 tokens
"constitutional" → ["const", "itu", "tional"] # 3 tokens
" the" → [" the"]                            # 1 token (with space)
```

Each token maps to an integer ID. The model embeds that ID into a vector.

**Why this matters:**
- Token count ≠ word count. Legal documents with rare words cost more tokens.
- Context window = max tokens the model can process at once (e.g., 4096 for many 7B models).
- Costs scale with token count, not characters.

---

## The Embedding Layer

Before attention, each token ID is converted to a dense vector via an **embedding matrix** (a giant lookup table, also learned during training).

```
token_id 5412 → row 5412 of embedding matrix → 4096-dimensional vector
```

This is where word meaning first enters. Similar tokens get similar vectors.

---

## Self-Attention: The Core Mechanism

For each token, attention computes: "which other tokens should I look at, and how much?"

Three learned projections per token:
- **Query (Q)**: "what am I looking for?"
- **Key (K)**: "what do I offer?"
- **Value (V)**: "what information do I provide?"

**Attention score** between token i and token j:
```
score(i, j) = softmax( Q_i · K_j / √d_k )
```

The output for token i is a weighted sum of all Value vectors, weighted by attention scores.

**Intuition**: `accused` queries for tokens that describe rights. `rights` has a matching key. High score. `accused` pulls in the information from `rights`.

---

## Multi-Head Attention

Run attention `h` times in parallel with different Q/K/V projections. Concatenate results.

Why: different heads can learn different types of relationships simultaneously.
- Head 1: syntactic subject-verb relationships
- Head 2: coreference (pronoun → noun)
- Head 3: document-level legal structure
- etc.

---

## The Full Transformer Block

```
Input
  → Layer Norm
  → Multi-Head Self-Attention
  → Add (residual connection)
  → Layer Norm
  → Feed-Forward Network (2 linear layers + activation)
  → Add (residual connection)
Output
```

**Residual connection**: adds the input to the output. Critical for training deep networks — gradients flow directly through, avoiding vanishing gradient.

**Feed-Forward Network**: two linear layers with GELU activation, 4× wider than the embedding dimension. This is where "factual knowledge" is thought to be stored.

A 7B model has 32 of these blocks stacked.

---

## The Language Model Head

After all transformer blocks: one final linear layer projects from embedding dimension → vocabulary size.

```
hidden_state (4096-dim) → vocab_logits (32000-dim) → softmax → probabilities
```

At each position, the model predicts the probability of every possible next token. Sampling (temperature, top-p) picks one.

---

## Positional Encoding

Attention is permutation-invariant — it doesn't know order. Positional encoding adds position information.

Modern models use **RoPE** (Rotary Position Embedding): rotates the Q and K vectors by an angle proportional to their position. Relative positions are encoded directly in the dot product.

---

## Context Window = Working Memory

The context window is how much the model "sees" at once. Everything outside it is invisible.

This is why retrieval is necessary for long documents: you can't fit the entire Civil Code (50k+ tokens) into a 4096-token context. You retrieve the relevant ~5 chunks and put those in context.

---

## Generation: Sampling One Token at a Time

```
prompt tokens → forward pass → logits → sample → new token
append new token → forward pass again → next token
...
```

**Key parameters you control:**
- `temperature`: 0 = greedy (always pick highest probability), 1 = sample normally, >1 = more random
- `top_p` (nucleus sampling): only consider tokens that make up top p% of probability mass
- `max_tokens`: hard stop

For legal reasoning: low temperature (0.1–0.3) for more deterministic, citation-accurate output.

---

## Base vs. Instruct vs. Chat Models

| Type | Trained to | Use for |
|------|-----------|---------|
| Base | Predict next token | Fine-tuning starting point |
| Instruct | Follow instructions (SFT) | Your use case |
| Chat | Multi-turn conversation (RLHF) | Chatbots |

`adrienbrault/saul-instruct-v1` = base Saul (legal domain) + instruction tuning. It follows the system prompt format.

---

## Why Architecture Variants Exist

| Model family | Innovation |
|-------------|-----------|
| LLaMA | Efficient: RoPE, SwiGLU, RMSNorm instead of LayerNorm |
| Mistral | Sliding window attention (longer effective context) |
| Gemma | Tied embeddings, novel normalization |
| Qwen | Extended vocab for CJK, MoE variants |

All are Transformers. The differences are engineering choices for speed, quality, and hardware efficiency.

---

## Connection to This Project

When `reason()` is called:
1. System prompt + evidence block + question → tokenizer → token IDs
2. Token IDs → embedding layer → vectors
3. 32 transformer blocks process the full sequence
4. Output logits at the last position → sample → first token of the answer
5. Repeat until `</s>` or `max_tokens`

The model "reasons" by attending to the evidence tokens at each generation step. Its attention heads literally look back at the legal passages to produce each output token.

---

## This Week's Code

1. `01_tokenization.py` — tokenize text, count tokens, see BPE in action
2. `02_attention_simplified.py` — attention from scratch in numpy
3. `03_generation_params.py` — effect of temperature on outputs

```bash
pip install transformers
python 01_tokenization.py
python 02_attention_simplified.py
python 03_generation_params.py
```
