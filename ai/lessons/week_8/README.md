# Week 8 — Agents, Tool Use, and LlamaIndex Orchestration

An agent is an LLM that can take actions, observe results, and decide what to do next — in a loop, until it reaches a goal.

This week covers: what agents are, why they matter, how to build them with LlamaIndex (your main framework), and how to wire the retrieve→reason→re-retrieve loop for the legal system.

---

## What Makes Something an Agent

A basic LLM call: prompt → response. One step. Stateless.

An agent: prompt → [decide action] → [take action] → [observe result] → [decide next action] → ... → final answer.

The loop + tools is what makes it an agent.

**Tool use**: the LLM can call functions you define. It decides which tool to call based on the question.

```
User: "What are the rights of an accused person in the Philippines?"

Agent thinks:
  → I need to search the legal documents first
  → [calls search_documents("rights accused person")]
  → Got 5 chunks. Let me reason over them.
  → [calls reason_from_evidence(question, chunks)]
  → Answer established from Article III Section 14
  → Return answer
```

The model decides when to call each tool. You define the tools.

---

## Agent Architectures

### ReAct (Reason + Act)
The most common pattern: alternate between Thought, Action, Observation.

```
Thought: I need to find the relevant constitutional provisions.
Action: search_documents("rights of accused Philippines")
Observation: [5 chunks returned from constitution.md]
Thought: The evidence covers Section 14. Let me reason over it.
Action: reason("What are rights of accused?", chunks)
Observation: established=True, answer="Under Section 14..."
Final Answer: Under Article III Section 14...
```

Each "Thought" is the LLM narrating its reasoning. Each "Action" calls a tool.

### OpenAI Function Calling Format
Modern way: the LLM outputs structured tool calls, not free-form text.

```json
{
  "tool": "search_documents",
  "arguments": {"query": "rights of accused", "k": 5}
}
```

Your code executes the tool, returns the result, and the LLM continues.

### Plan-and-Execute
For complex multi-step tasks:
1. **Planner**: LLM generates a plan (list of steps) upfront
2. **Executor**: executes each step, using specialized tools or sub-agents

Better for tasks that need global coherence (legal brief that must cover 5 specific issues).

---

## LlamaIndex: Your Orchestration Framework

LlamaIndex handles:
- Tool calling infrastructure
- Agent loop management
- Memory and state between steps
- Pipeline composition

### QueryPipeline: Deterministic Chains

For predictable, fixed pipelines (no branching):

```python
from llama_index.core.query_pipeline import QueryPipeline, InputComponent
from llama_index.core.query_pipeline import FnComponent

def retrieve_fn(question: str) -> list:
    return retrieve(question, k=5)

def reason_fn(question: str, chunks: list) -> ReasoningResult:
    return reason(question, chunks)

pipeline = QueryPipeline()
pipeline.add_modules({
    "input": InputComponent(),
    "retriever": FnComponent(fn=retrieve_fn),
    "reasoner": FnComponent(fn=reason_fn),
})
pipeline.add_link("input", "retriever", src_key="question", dest_key="question")
pipeline.add_link("input", "reasoner", src_key="question", dest_key="question")
pipeline.add_link("retriever", "reasoner", src_key="output", dest_key="chunks")

result = pipeline.run(question="What are the rights of an accused?")
```

The pipeline handles the data flow. You define the components.

### AgentRunner: The Loop

For dynamic behavior (when to re-retrieve depends on what was found):

```python
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool

search_tool = FunctionTool.from_defaults(
    fn=retrieve,
    name="search_legal_documents",
    description="Search indexed Philippine legal documents for relevant passages.",
)

agent = ReActAgent.from_tools(
    tools=[search_tool],
    llm=your_llm,
    verbose=True,
)

response = agent.chat("What rights does an accused have?")
```

The agent decides when to search and when to stop.

---

## The Retrieve → Reason → Re-retrieve Loop

The core loop for your legal system:

```
Question
    ↓
retrieve(question, k=5)
    ↓
reason(question, chunks)
    ↓
result.established?
  YES → return answer
  NO  → generate refined query from what's missing
          → retrieve(refined_query, k=5)
          → reason(question, original_chunks + new_chunks)
          → return answer (or "not established" if still missing)
```

The "not established" case is informative: the model explains *what* is missing. Use that as the next search query.

```python
def query_with_loop(question: str, max_attempts: int = 2) -> ReasoningResult:
    all_chunks = retrieve(question, k=5)
    result = reason(question, all_chunks)

    for _ in range(max_attempts - 1):
        if result.established:
            break
        refined = f"{question}\nLooking specifically for: {result.answer}"
        new_chunks = retrieve(refined, k=3)
        all_chunks = deduplicate(all_chunks + new_chunks)
        result = reason(question, all_chunks)

    return result
```

---

## Memory in Agents

By default, each call is stateless. For multi-turn conversations, you need memory.

LlamaIndex `ChatMemoryBuffer`: stores conversation history, truncates at context limit.

```python
from llama_index.core.memory import ChatMemoryBuffer

memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
agent = ReActAgent.from_tools(tools, llm=llm, memory=memory)

agent.chat("What are the rights of an accused?")
agent.chat("Can they waive those rights?")  # agent remembers previous answer
```

For legal consultations with follow-up questions, this is essential.

---

## Multi-Agent Patterns

As systems grow more complex:

### Supervisor + Specialists
```
User question
    ↓
Supervisor Agent (routes to specialist)
    ├→ Civil Law Agent (handles property, contracts, family)
    ├→ Constitutional Law Agent (handles rights, government)
    └→ Criminal Law Agent (handles criminal procedure)
```

### Parallel Research
```
Question: "Is this contract valid given X, Y, and Z?"
    ├→ Agent 1: research X
    ├→ Agent 2: research Y
    └→ Agent 3: research Z
    ↓
Synthesis agent: combine results, answer question
```

LlamaIndex's workflow system supports these patterns.

---

## Tool Design Principles

**1. One tool = one clear capability**
Bad: `legal_tool(action: str, query: str)` — the LLM must know what `action` values exist.
Good: separate `search_constitution(query)` and `search_civil_code(query)`.

**2. Descriptive names and docstrings**
The LLM reads the tool description to decide whether to use it. Write it for the LLM, not just for humans.

```python
def search_constitution(query: str) -> list[EvidenceChunk]:
    """Search the 1987 Philippine Constitution for relevant passages.
    Use this when the question involves fundamental rights, government structure,
    or constitutional provisions."""
```

**3. Return structured data**
Return dicts or dataclasses, not raw strings. The LLM can extract specific fields.

---

## Connection to This Project

The retrieve → reason → loop IS the agent. Currently it's implemented as a direct function call. This week you wrap it in LlamaIndex's QueryPipeline to get:
- Clean composition
- Logging and tracing
- Easy swapping of components
- The re-retrieve loop via `RetryQueryEngine`

Layer 7 of the architecture is this orchestration layer. FastAPI (Week 7) wraps the outer edge.

---

## This Week's Code

1. `01_tool_use.py` — define tools, let an LLM decide which to call
2. `02_react_agent.py` — ReAct agent with search and reason tools
3. `03_llamaindex_pipeline.py` — deterministic QueryPipeline for the legal system
4. `04_retrieve_reason_loop.py` — re-retrieve loop with max attempts

```bash
pip install llama-index-core
python 01_tool_use.py
python 03_llamaindex_pipeline.py
python 04_retrieve_reason_loop.py
```
