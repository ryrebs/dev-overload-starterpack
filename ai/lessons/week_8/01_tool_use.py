"""
Week 8 — Tool use: let an LLM decide which function to call.

The LLM reads tool descriptions and decides when and how to use them.
This is the foundation of agent behavior.
"""

import json
import sys
from pathlib import Path
from openai import OpenAI

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

client = OpenAI(base_url="http://127.0.0.1:11434/v1", api_key="ollama")
MODEL = "adrienbrault/saul-instruct-v1:Q8_0"


# --- Define tools ---

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_legal_documents",
            "description": (
                "Search indexed Philippine legal documents for relevant passages. "
                "Use this when you need to find specific legal provisions, articles, or sections."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant legal passages",
                    },
                    "k": {
                        "type": "integer",
                        "description": "Number of passages to return (default 5)",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_document_list",
            "description": "Get a list of all indexed legal documents.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
]


def search_legal_documents(query: str, k: int = 5) -> str:
    """The actual implementation of the search tool."""
    from retrieval import retrieve
    chunks = retrieve(query, k=k)
    if not chunks:
        return "No relevant passages found."
    results = []
    for i, c in enumerate(chunks, 1):
        results.append(f"[{i}] Source: {c.source} (score={c.score:.3f})\n{c.text[:200]}...")
    return "\n\n".join(results)


def get_document_list() -> str:
    return "Indexed documents:\n- constitution.md (1987 Philippine Constitution)\n- civil_code.md (Civil Code of the Philippines)"


def execute_tool(tool_name: str, arguments: dict) -> str:
    if tool_name == "search_legal_documents":
        return search_legal_documents(**arguments)
    elif tool_name == "get_document_list":
        return get_document_list()
    return f"Unknown tool: {tool_name}"


def agent_loop(question: str, max_steps: int = 5) -> str:
    """Run the tool-use loop: model decides when to call tools and when to answer."""
    messages = [
        {
            "role": "system",
            "content": "You are a Philippine legal assistant. Use tools to search documents, then answer.",
        },
        {"role": "user", "content": question},
    ]

    print(f"Question: {question}\n")

    for step in range(max_steps):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            max_tokens=500,
            temperature=0.0,
        )

        msg = response.choices[0].message
        finish_reason = response.choices[0].finish_reason

        if finish_reason == "tool_calls" and msg.tool_calls:
            messages.append(msg)  # Add assistant message with tool calls

            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                print(f"[Step {step+1}] Tool call: {name}({args})")

                result = execute_tool(name, args)
                print(f"  Result: {result[:100]}...\n")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })
        else:
            # Model is done using tools, returning final answer
            print(f"[Step {step+1}] Final answer:")
            return msg.content

    return "Reached maximum steps without a final answer."


if __name__ == "__main__":
    questions = [
        "What documents do you have indexed?",
        "What are the rights of an accused person?",
    ]
    for q in questions:
        answer = agent_loop(q)
        print(f"Answer: {answer}\n{'='*60}\n")
