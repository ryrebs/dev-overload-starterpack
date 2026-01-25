import asyncio
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.ollama import Ollama


# Define a simple calculator tool
def multiply(a: float, b: float) -> float:
    """Useful for multiplying two numbers."""
    return a * b


def get_master_name():
    """Return the master's name when asked"""
    return "Human Master"


# Create an agent workflow with our calculator tool
agent = FunctionAgent(
    tools=[multiply, get_master_name],
    llm=Ollama(
        model="qwen3:8b",
        request_timeout=360.0,
        # Manually set the context window to limit memory usage
        context_window=8000,
    ),
    system_prompt="You are a helpful assistant that will assist the stupid human.",
)


async def main():
    # Run the agent
    response = await agent.run("What is 1 * 2?")
    print(str(response))

    response = await agent.run("What is your master's name?")
    print(str(response))


# Run the agent
if __name__ == "__main__":
    asyncio.run(main())
