"""
Week 2 — Self-attention from scratch.

Implements the core attention mechanism in ~40 lines of numpy.
This is what runs inside every transformer layer.
"""

import numpy as np


def softmax(x: np.ndarray) -> np.ndarray:
    """Numerically stable softmax."""
    x = x - x.max(axis=-1, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=-1, keepdims=True)


def attention(Q: np.ndarray, K: np.ndarray, V: np.ndarray) -> tuple:
    """
    Scaled dot-product attention.

    Args:
        Q: queries  (seq_len, d_k)
        K: keys     (seq_len, d_k)
        V: values   (seq_len, d_v)

    Returns:
        output: (seq_len, d_v)
        weights: attention weights (seq_len, seq_len)
    """
    d_k = Q.shape[-1]

    # Similarity between each query and all keys
    scores = Q @ K.T / np.sqrt(d_k)   # (seq_len, seq_len)

    # Convert to probabilities (sums to 1 per query)
    weights = softmax(scores)           # (seq_len, seq_len)

    # Weighted sum of values
    output = weights @ V                # (seq_len, d_v)

    return output, weights


def multi_head_attention(x: np.ndarray, n_heads: int, d_model: int) -> np.ndarray:
    """
    Multi-head attention with random weights (not trained).
    Demonstrates the structure; in a real model, weights are learned.
    """
    d_k = d_model // n_heads
    seq_len = x.shape[0]

    all_heads = []
    for _ in range(n_heads):
        # Each head has its own Q, K, V projection matrices (learned in practice)
        W_Q = np.random.randn(d_model, d_k) * 0.1
        W_K = np.random.randn(d_model, d_k) * 0.1
        W_V = np.random.randn(d_model, d_k) * 0.1

        Q = x @ W_Q  # (seq_len, d_k)
        K = x @ W_K
        V = x @ W_V

        head_output, _ = attention(Q, K, V)
        all_heads.append(head_output)

    # Concatenate all heads
    concatenated = np.concatenate(all_heads, axis=-1)  # (seq_len, d_model)
    return concatenated


if __name__ == "__main__":
    print("=== Attention Mechanism Demo ===\n")

    # Simple example: 4 tokens, 8-dimensional embeddings
    np.random.seed(42)
    seq_len = 4
    d_model = 8
    d_k = 4

    # Simulate token embeddings for: ["the", "accused", "has", "rights"]
    # In practice, these come from the embedding matrix
    token_embeddings = np.random.randn(seq_len, d_model)

    # Random projection matrices (in real models, these are learned)
    W_Q = np.random.randn(d_model, d_k)
    W_K = np.random.randn(d_model, d_k)
    W_V = np.random.randn(d_model, d_k)

    Q = token_embeddings @ W_Q
    K = token_embeddings @ W_K
    V = token_embeddings @ W_V

    output, weights = attention(Q, K, V)

    tokens = ["the", "accused", "has", "rights"]
    print("Attention weights (row = query token, col = key token):")
    print("Higher weight = 'query token attends more to key token'\n")
    print(f"{'':10s}", end="")
    for t in tokens:
        print(f"{t:10s}", end="")
    print()
    for i, row_token in enumerate(tokens):
        print(f"{row_token:10s}", end="")
        for j in range(len(tokens)):
            print(f"{weights[i, j]:.3f}     ", end="")
        print()

    print(f"\nEach row sums to 1: {weights.sum(axis=1).round(4)}")
    print(f"\nOutput shape: {output.shape} (same seq_len, transformed representation)")

    print("\n=== Multi-Head Attention ===")
    print("4 heads, each attending to different relationship types\n")

    mha_output = multi_head_attention(token_embeddings, n_heads=4, d_model=8)
    print(f"Input shape:  {token_embeddings.shape}")
    print(f"Output shape: {mha_output.shape}")
    print("Same shape — different internal representations combined.")
