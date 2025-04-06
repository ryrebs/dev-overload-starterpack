from bs4 import SoupStrainer
from typing import List
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langchain_core.documents import Document
from langchain_core.runnables import chain


target_url = "https://blog.langchain.dev/using-langsmith-to-support-fine-tuning-of-open-source-llms/"


@tool(response_format="content")
def search_info(query: str):
    """Retrieve a information about fine tuning"""
    ## Only keep post title, headers, and content from the full HTML.
    ## This is specific only to the target_url for
    ## demontration purposes only
    bs4_strainer = SoupStrainer("p")
    loader = WebBaseLoader(
        web_paths=(target_url,),
        bs_kwargs={"parse_only": bs4_strainer},
    )
    docs = loader.load()
    assert len(docs) == 1

    content = docs[0].page_content
    return content


@chain
def retriever(query: str) -> List[Document]:
    """Retriever is a function that accepts a query and returns a list of relevant
    documents based on the query
    """

    return vector_store.similarity_search(query, k=1)


## Retriever usage
docs = retriever.batch(
    [
        "How many distribution centers does Nike have in the US?",
        "When was Nike incorporated?",
    ],
)
## Vector store can also generate its own retriever
## see docs for more info.


if __name__ == "__main__":
    # Init model
    chat_model = init_chat_model(model="qwen2.5:7b", model_provider="ollama")

    # Attach tool
    model_with_tools = chat_model.bind_tools([search_info])

    message_wo_tool = HumanMessage(content="hi!")
    message_w_tool = HumanMessage(content="Search the web on how to fine tune?")

    ## Without setup agent
    ## Response with tool calling
    # response = model_with_tools.invoke([HumanMessage(content="hi!")])
    # print(f"ContentString: {response.content}")
    # print(f"ToolCalls: {response.tool_calls}")

    ## Response with tool calling
    ## The better the model, the better it decides whether
    ## tool calling is needed, else play with your message
    # response = model_with_tools.invoke(
    #     [HumanMessage(content="Search the web on how to fine tune?")]
    # )
    # print(f"ContentString: {response.content}")
    # print(f"ToolCalls: {response.tool_calls}")

    ## Agent setup
    agent_executor = create_react_agent(chat_model, [search_info])

    ## print directly after the all processes executes
    # response = agent_executor.invoke({"messages": [message_w_tool]})
    # print(response["messages"])

    ## Or stream after each process executes or a response is available
    for step in agent_executor.stream(
        {"messages": [message_w_tool]},
        stream_mode="values",
    ):
        step["messages"][-1].pretty_print()
