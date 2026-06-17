"""
Week 8 — ReAct agent: Reason + Act loop with LlamaIndex.

The agent alternates between Thought (reasoning) and Action (tool calls)
until it has enough information to give a final answer.

ReAct is the most common agent architecture for Q&A and research tasks.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.core.llms import LLM
from llama_index.llms.openai_like import OpenAILike

from retrieval import retrieve, EvidenceChunk


# --- Define tools the agent can use ---

def search_constitution(query: str, k: int = 3) -> str:
    """
    Search the 1987 Philippine Constitution for relevant provisions.
    Use this when the question involves fundamental rights, government structure,
    or constitutional provisions.
    """
    chunks = retrieve(query, k=k)
    const_chunks = [c for c in chunks if "constitution" in c.source.lower()]
    if not const_chunks:
        return "No relevant constitutional provisions found."
    return "\n\n".join(f"[{c.source}] {c.text[:300]}" for c in const_chunks[:3])


def search_civil_code(query: str, k: int = 3) -> str:
    """
    Search the Philippine Civil Code for relevant articles.
    Use this when the question involves contracts, property, family law,
    obligations, or civil law generally.
    """
    chunks = retrieve(query, k=k)
    civil_chunks = [c for c in chunks if "civil" in c.source.lower()]
    if not civil_chunks:
        return "No relevant Civil Code articles found."
    return "\n\n".join(f"[{c.source}] {c.text[:300]}" for c in civil_chunks[:3])


def search_all_documents(query: str, k: int = 5) -> str:
    """
    Search all indexed Philippine legal documents.
    Use this when you're not sure which document contains the answer,
    or when the question spans multiple areas of law.
    """
    chunks = retrieve(query, k=k)
    if not chunks:
        return "No relevant documents found."
    return "\n\n".join(f"[{i+1}] {c.source}: {c.text[:250]}" for i, c in enumerate(chunks))


# Wrap functions as LlamaIndex tools
tools = [
    FunctionTool.from_defaults(fn=search_constitution),
    FunctionTool.from_defaults(fn=search_civil_code),
    FunctionTool.from_defaults(fn=search_all_documents),
]

# LLM via Ollama
llm = OpenAILike(
    model="adrienbrault/saul-instruct-v1:Q8_0",
    api_base="http://127.0.0.1:11434/v1",
    api_key="ollama",
    is_chat_model=True,
    temperature=0.1,
    max_tokens=800,
)

# Build the ReAct agent
agent = ReActAgent.from_tools(
    tools=tools,
    llm=llm,
    verbose=True,          # shows Thought/Action/Observation steps
    max_iterations=5,      # prevent infinite loops
)


def run_agent(question: str) -> str:
    print(f"\n{'='*60}")
    print(f"QUESTION: {question}")
    print(f"{'='*60}\n")
    response = agent.chat(question)
    return str(response)


if __name__ == "__main__":
    questions = [
        "What are the rights of an accused person?",
        "Can a 17-year-old enter a valid contract?",
    ]

    for q in questions:
        answer = run_agent(q)
        print(f"\nFINAL ANSWER: {answer[:400]}...")
        print()

    print("\n=== Agent Architecture: ReAct ===")
    print("Thought: What do I need to know?")
    print("Action:  Call a tool (search_constitution, search_civil_code)")
    print("Observation: Read the tool result")
    print("Thought: Do I have enough information? If yes, answer. If no, search more.")
    print("\nEach agent step = one LLM call. The loop runs until the agent decides to answer.")
