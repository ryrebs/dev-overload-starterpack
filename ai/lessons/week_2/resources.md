# Week 2 Resources

## Must-Read
- **Illustrated Transformer (Jay Alammar)** — the best visual explanation of transformers
- **Attention Is All You Need (Vaswani et al., 2017)** — the original paper. Read the abstract and sections 3.1-3.3.
- **Andrej Karpathy: Let's build GPT from scratch** — 2-hour video. Build a miniGPT in pure PyTorch.

## Reference
- **HuggingFace Tokenizers docs** — how BPE works
- **LLaMA 2 paper** — modern transformer architecture details (RoPE, SwiGLU, RMSNorm)

## Practice
- Modify `02_attention_simplified.py` to add a causal mask (future tokens cannot attend to future tokens — this is how GPT works)
- Try the `gpt2` model from HuggingFace to generate text and observe temperature effects

## What Interviewers Ask
- "Explain attention in one sentence."
- "What does temperature control in generation?"
- "Why do we divide by sqrt(d_k) in attention?"
- "What's the difference between an encoder and a decoder transformer?"
