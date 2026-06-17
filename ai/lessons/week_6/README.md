# Week 6 — Evaluation and Benchmarking

This is the week that separates hobbyists from engineers. Anyone can build a RAG pipeline. The engineer measures whether it works.

---

## Why Evaluation Is Non-Negotiable

Without evaluation:
- You don't know if retrieval is finding the right chunks
- You don't know if the reasoning model is using the evidence correctly
- You can't tell if a prompt change improved things or made them worse
- You can't tell if a new embedding model is better

With evaluation:
- You have a number. You changed something. The number went up or down. You know what happened.

---

## What to Evaluate

There are two things that can fail. Measure them separately.

### 1. Retrieval Quality

Does `retrieve(question)` return the right chunks?

**Metrics:**
- **Recall@k**: of the relevant chunks that exist, how many did the retriever find in the top k?
- **Precision@k**: of the top k chunks returned, how many were actually relevant?
- **MRR (Mean Reciprocal Rank)**: where did the first relevant result appear?

Example:
```
Question: "What is the age of majority?"
Relevant chunk: Civil Code Article 234
Retriever returned: [Article 2, Article 234, Article 1, Article 5, Article 9]
                                    ^ position 2

Recall@5 = 1/1 = 100% (found the relevant chunk in top 5)
MRR = 1/2 = 0.5 (relevant chunk was at position 2)
```

### 2. Reasoning Quality

Given the correct chunks, does the model answer correctly?

**Metrics:**
- **Answer accuracy**: is the answer factually correct per the source?
- **Citation accuracy**: do the cited quotes actually appear verbatim in the retrieved chunks?
- **Established flag accuracy**: is `established` True when the answer can be derived, False when it cannot?

---

## Building a Golden Dataset

A **golden dataset** (also called a test set or eval set) is a collection of question-answer pairs where the correct answer is known.

For your project:
```python
golden = [
    {
        "question": "What is the age of majority in the Philippines?",
        "expected_chunks": ["civil_code.md:Article 234"],
        "expected_answer_contains": ["18", "eighteen"],
        "expected_established": True,
    },
    {
        "question": "What rights does an accused person have?",
        "expected_chunks": ["constitution.md:Article III Section 14"],
        "expected_established": True,
    },
    {
        "question": "What is the penalty for jaywalking?",
        "expected_chunks": [],  # not in our documents
        "expected_established": False,
    },
]
```

**How to build it:**
1. Read through your indexed documents
2. Write 20–50 questions whose answers you can verify
3. Include "not in the documents" questions (5–10) to test `established=False`
4. Include questions that require combining two chunks (tests multi-hop reasoning)

20 questions is enough to start. 50 is solid. 200 is production-grade.

---

## LLM-as-Judge

For open-ended answers, you can't do exact string matching. Use another LLM to judge quality.

```
Judge prompt:
"Here is a legal question, the expected answer, and the model's answer.
Score 0-3: 0=wrong, 1=partially right, 2=correct, 3=correct with good citation.
Question: {q}
Expected: {expected}
Model answer: {actual}
Score:"
```

**Cautions:**
- LLM judges are biased toward longer, more confident answers
- They can be manipulated by style (use a different model than the one being judged)
- They're better at relative ranking than absolute scoring
- Always spot-check a sample manually

LLM-as-judge is useful for fast iteration, not final ground truth.

---

## RAGAS: Automated RAG Evaluation

RAGAS is a library specifically for evaluating RAG pipelines.

**Key metrics it computes:**
- **Faithfulness**: does the answer contain claims supported by the retrieved context?
- **Answer Relevancy**: is the answer relevant to the question?
- **Context Recall**: does the retrieved context contain the information needed?
- **Context Precision**: is the retrieved context concise (not full of irrelevant chunks)?

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

result = evaluate(
    dataset=eval_dataset,
    metrics=[faithfulness, answer_relevancy],
)
```

RAGAS uses an LLM internally for some metrics. Works with Ollama.

---

## The Eval Loop

```
Build golden dataset
    ↓
Run pipeline on all questions
    ↓
Compute Recall@5 (retrieval), Faithfulness (reasoning)
    ↓
Identify failure modes:
  - Low recall → chunking too coarse? wrong embedding model?
  - Low faithfulness → model ignoring evidence? prompts too weak?
    ↓
Make one change
    ↓
Re-run eval → compare numbers
    ↓
Repeat
```

Only change one variable at a time. Otherwise you don't know which change helped.

---

## Connection to This Project

Your golden dataset should include:
1. Civil Code questions (property, contracts, family law)
2. Constitution questions (rights, structure of government)
3. Cross-document questions (where both documents are needed)
4. Out-of-scope questions (test `established=False`)

Once you have ~20 golden questions, you have a regression test: every time you change the system prompt, embedding model, or chunking strategy, you run it and see if the score went up or down.

This is your portfolio's strongest differentiator. Most tutorials stop at "it works." You have a number.

---

## This Week's Code

1. `01_golden_dataset.py` — create and store a golden dataset for the legal project
2. `02_retrieval_metrics.py` — compute Recall@k and MRR against the golden set
3. `03_llm_judge.py` — use an LLM to score answer quality

```bash
pip install ragas datasets
python 01_golden_dataset.py
python 02_retrieval_metrics.py
python 03_llm_judge.py
```
