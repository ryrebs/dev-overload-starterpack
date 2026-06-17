# Week 8 Resources

## Must-Read
- **ReAct paper (Yao et al., 2023)** — the original Reason + Act framework
- **LlamaIndex Agents docs** — ReActAgent, FunctionCallingAgent, custom tools
- **LlamaIndex QueryPipeline** — composable pipeline documentation

## Reference
- **OpenAI function calling docs** — the tool call format used by most models
- **LangGraph** (alternative to LlamaIndex for agents) — if you want to explore graph-based control flow
- **Semantic Kernel** — Microsoft's agent framework (good for enterprise)

## Agent Architecture Patterns
- **ReAct** — Thought → Action → Observation loop (use for exploration tasks)
- **Plan-and-Execute** — Plan upfront, execute step by step (use for structured tasks)
- **Reflexion** — Agent reflects on its own output and improves (use for quality-critical tasks)
- **Multi-agent** — Supervisor routes to specialist agents (use for complex domain tasks)

## Practice
- Extend `04_retrieve_reason_loop.py` to log every attempt and the refinement queries
- Build a multi-turn agent with memory: user asks follow-up questions, agent remembers context
- Add a "document list" tool so the agent can choose which source to search

## What Interviewers Ask
- "What is an agent vs. a simple LLM call?"
- "What is ReAct and when would you use it?"
- "How do you prevent an agent from running in an infinite loop?"
- "What are the failure modes of tool-using agents?"
