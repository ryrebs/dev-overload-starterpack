from llama_index.core import (
    StorageContext,
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
)
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.workflow import Context


import chromadb

import asyncio
import os
from datetime import datetime
from zoneinfo import ZoneInfo


# set up ChromaVectorStore and load in data
db = chromadb.PersistentClient(path="./basic_rag_data_db")
chroma_collection = db.get_or_create_collection("basic_rag")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


## Set up embedding model
Settings.embed_model = OllamaEmbedding(model_name="qwen3:8b")


## Q/A model
Settings.llm = Ollama(
    model="qwen3:8b",
    request_timeout=360.0,
    # Manually set the context window to limit memory usage
    context_window=8000,
)

## Load the data source
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
)

query_engine = index.as_query_engine()


## Tools
async def get_today_date():
    """Returns philippines date today"""
    return str(datetime.now(ZoneInfo("Asia/Manila")).date())


async def search_documents(query: str) -> str:
    """Answers questions about holidays in the philippines"""
    response = await query_engine.aquery(query)
    return str(response)


# Create an enhanced workflow with both tools
agent = AgentWorkflow.from_tools_or_functions(
    [get_today_date, search_documents],
    llm=Settings.llm,
    system_prompt="""Answer human questions and used the available tools like getting the date and holiday data""",
)

# Context is helpful if you want the agent to use pass conversation
ctx = Context(agent)


# Now we can ask questions about the documents or do calculations
async def main():
    response = await agent.run(
        "What is date today in the philippines?",
        ctx=ctx,
    )
    await ctx.store.set("date_info", response)
    response = await agent.run(
        "Is it holiday today in the philippines?",
        ctx=ctx,
    )
    print(response)


# Run the agent
if __name__ == "__main__":
    asyncio.run(main())
