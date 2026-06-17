"""
Week 2 — Tokenization: what the model actually sees.

Demonstrates how text is split into tokens, how token count differs from word count,
and why this matters for context window budgeting.
"""

from transformers import AutoTokenizer


def show_tokens(tokenizer, text: str):
    """Show the token breakdown for a piece of text."""
    tokens = tokenizer.encode(text)
    token_strs = [tokenizer.decode([t]) for t in tokens]
    print(f"Text: {repr(text)}")
    print(f"Token IDs: {tokens}")
    print(f"Tokens: {token_strs}")
    print(f"Count: {len(tokens)} tokens for {len(text.split())} words")
    print()


if __name__ == "__main__":
    # Use a small tokenizer that doesn't need a model download
    # This is the tokenizer used by many instruction models
    print("Loading tokenizer (LLaMA-style)...")
    try:
        tokenizer = AutoTokenizer.from_pretrained("hf-internal-testing/llama-tokenizer")
    except Exception:
        # Fallback: use GPT-2 tokenizer which is always available
        print("Using GPT-2 tokenizer as fallback...")
        tokenizer = AutoTokenizer.from_pretrained("gpt2")

    print("=" * 60)
    print("TOKENIZATION EXAMPLES")
    print("=" * 60)
    print()

    examples = [
        "The accused has the right to be presumed innocent.",
        "Constitution",
        "constitutional",
        "unconstitutionality",
        "Article III Section 14",
        "We, the sovereign Filipino people",
        # Note: rare/legal words often split more
        "Jurisprudence establishes the parameters of constitutionality.",
        "habeas corpus",
        "mandamus",
    ]

    for text in examples:
        show_tokens(tokenizer, text)

    # Context window budgeting example
    print("=" * 60)
    print("CONTEXT WINDOW BUDGETING")
    print("=" * 60)
    print()

    system_prompt = """You are a legal reasoning assistant. Base every answer strictly
on the evidence passages provided. Cite exact passages."""

    evidence_chunk = """[1] Source: constitution.md
    Section 14. (1) No person shall be held to answer for a criminal offense without
    due process of law. (2) In all criminal prosecutions, the accused shall be presumed
    innocent until the contrary is proved, and shall enjoy the right to be heard by
    himself and counsel, to be informed of the nature and cause of the accusation
    against him, to have a speedy, impartial, and public trial..."""

    question = "What are the rights of an accused person under Philippine law?"

    # A 7B model often has a 4096-token context
    context_limit = 4096
    reserved_for_response = 512

    prompt_tokens = (
        len(tokenizer.encode(system_prompt)) +
        len(tokenizer.encode(evidence_chunk)) +
        len(tokenizer.encode(question))
    )

    print(f"System prompt:     {len(tokenizer.encode(system_prompt)):4d} tokens")
    print(f"Evidence (1 chunk):{len(tokenizer.encode(evidence_chunk)):4d} tokens")
    print(f"Question:          {len(tokenizer.encode(question)):4d} tokens")
    print(f"Total prompt:      {prompt_tokens:4d} tokens")
    print(f"Context limit:     {context_limit:4d} tokens")
    print(f"Reserved response: {reserved_for_response:4d} tokens")
    print(f"Budget for evidence: {context_limit - reserved_for_response - len(tokenizer.encode(system_prompt)) - len(tokenizer.encode(question)):4d} tokens")
    print(f"\nAt ~400 tokens/chunk, you can fit ~{(context_limit - reserved_for_response - len(tokenizer.encode(system_prompt))) // 400} evidence chunks.")
