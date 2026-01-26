import logging
import sys
from IPython.display import Markdown, display

import pandas as pd
from llama_index.experimental.query_engine import PandasQueryEngine

import asyncio
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core import (
    Settings,
)
from llama_index.llms.ollama import Ollama


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


# Build or get your df
df = pd.DataFrame(
    {
        "city": ["Toronto", "Tokyo", "Berlin"],
        "population": [1, 0, -1],
    }
)
Settings.llm = Ollama(
    model="codellama:13b",
    request_timeout=360.0,
    # Manually set the context window to limit memory usage
    context_window=8000,
)

query_engine = PandasQueryEngine(
    df=df, verbose=True, llm=Settings.llm, synthesize_response=True
)


# Run the agent
if __name__ == "__main__":
    query = "What is the city with th'e highest population?"

    response = query_engine.query(query)

    ## How pandas come up with the answer
    # print(response.metadata["pandas_instruction_str"])

    ## With synthesize_response
    ## The city with the highest population is _.

    ## Note: Better llm avoids generating wrong syntax
    print(response)
