# Week 5 Resources

## Must-Read
- **Prompting Guide (promptingguide.ai)** — comprehensive free resource
- **instructor docs** — structured output with Pydantic
- **OWASP LLM Top 10** — security risks including prompt injection

## Reference
- **Few-shot learning with LLMs (Brown et al.)** — the original GPT-3 paper demonstrating few-shot
- **Chain-of-Thought Prompting (Wei et al.)** — the CoT paper

## Practice
- Improve the system prompt in `reasoning.py` to reduce `established=False` false negatives
- Add a few-shot example to the reasoning prompt using an actual chunk from your documents
- Try to get the LLM to follow the `ReasoningResult` schema without instructor (manually add JSON instructions)

## What Interviewers Ask
- "What is prompt injection and how do you defend against it?"
- "When would you use few-shot vs. fine-tuning?"
- "What is structured output and why does it matter in production?"
- "How do you test whether a prompt change improved things?"
