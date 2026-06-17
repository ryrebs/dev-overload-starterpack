# Week 6 Resources

## Must-Read
- **RAGAS paper** — Retrieval Augmented Generation Assessment
- **BEIR benchmark** — how to build proper retrieval evaluation sets
- **G-Eval paper** — LLM-as-judge with chain-of-thought scoring

## Reference
- **ragas library docs** — faithfulness, answer relevancy, context recall metrics
- **MLflow** — experiment tracking (log eval runs, compare prompt versions)

## Practice
- Expand the golden dataset to 30 questions
- Add a metric for citation accuracy: do the quoted passages actually appear in the chunks?
- Track eval scores as you change the system prompt — plot improvement over time

## What Interviewers Ask
- "How would you evaluate a RAG system before putting it in production?"
- "What is the difference between precision and recall in retrieval?"
- "What is LLM-as-judge and what are its limitations?"
- "How do you know your embedding model is right for your domain?"
