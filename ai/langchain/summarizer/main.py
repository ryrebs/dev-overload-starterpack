import asyncio
from langchain_community.document_loaders import WebBaseLoader
from langchain.chat_models import init_chat_model
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import CharacterTextSplitter
import operator
from typing import Annotated, List, Literal, TypedDict
from langchain.chains.combine_documents.reduce import (
    acollapse_docs,
    split_list_of_docs,
)
from langchain_core.documents import Document
from langgraph.constants import Send
from langgraph.graph import END, START, StateGraph


## LLM
llm = init_chat_model(model="mistral", model_provider="ollama")

## Hypothetical llm token's max limit
## for demonstrating collapsing steps
token_max = 1000

# Define prompt
prompt = ChatPromptTemplate.from_messages(
    [("system", "Write a concise summary of the following:\\n\\n{context}")]
)


## Source
def load_source():
    loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
    docs = loader.load()
    return docs


## Summarizing by stuff or feeding all tokens
## the the llm to summarize it.
## NOTE: Tokens should fit into the token context of the llm.
def stuff_summary(docs):

    # Instantiate chain
    chain = create_stuff_documents_chain(llm, prompt)

    # Invoke chain
    result = chain.invoke({"context": docs})
    print(result)


def split_docs(docs):
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    split_docs = text_splitter.split_documents(docs)
    return split_docs


## Summarizing by map reduce.
## It works by creating a chunks of summary of the whole source
## then creating a whole summary from each chunks of summary.
def map_reduce_summary(docs):
    # Also available via the hub: `hub.pull("rlm/reduce-prompt")`

    ## In order to create chunk of summary
    ## we need to split the source into chunks of documents
    more_docs = split_docs(docs)
    print(f"Generated {len(more_docs)} documents.")


def length_function(documents: List[Document]) -> int:
    """Get number of tokens for input contents."""
    return sum(llm.get_num_tokens(doc.page_content) for doc in documents)


# This will be the overall state of the main graph.
# It will contain the input document contents, corresponding
# summaries, and a final summary.
class OverallState(TypedDict):
    contents: List[str]
    # Notice here we use the operator.add
    # This is because we want combine all the summaries we generate
    # from individual nodes back into one list - this is essentially
    # the "reduce" part
    summaries: Annotated[
        list, operator.add  ## This is an annotation that langchain graph understands
    ]
    collapsed_summaries: List[Document]
    final_summary: str


# This will be the state of the node that we will "map" all
# documents to in order to generate summaries
class SummaryState(TypedDict):
    content: str


# Here we generate a summary, given a document
async def generate_summary(state: SummaryState):
    prompt = ChatPromptTemplate.from_messages(
        [("system", "Write a concise summary of the following:\\n\\n{context}")]
    ).invoke(state["content"])
    response = await llm.ainvoke(prompt)
    return {"summaries": [response.content]}


def map_summaries(state: OverallState):
    return [
        Send("generate_summary", {"content": content}) for content in state["contents"]
    ]


def collect_summaries(state: OverallState):
    return {
        "collapsed_summaries": [Document(summary) for summary in state["summaries"]]
    }


async def _reduce(input: dict) -> str:
    reduce_template = """
    The following is a set of summaries:
    {docs}
    Take these and distill it into a final, consolidated summary
    of the main themes.
    """
    reduce_prompt = ChatPromptTemplate([("human", reduce_template)])
    prompt = reduce_prompt.invoke(input)
    response = await llm.ainvoke(prompt)
    return response.content


# Add node to collapse summaries
async def collapse_summaries(state: OverallState):
    ## Split the docs into sub docs
    doc_lists = split_list_of_docs(
        state["collapsed_summaries"], length_function, token_max
    )

    ## Tell llm to summarize the sub docs
    results = []
    for doc_list in doc_lists:
        results.append(await acollapse_docs(doc_list, _reduce))

    return {"collapsed_summaries": results}


def should_collapse(
    state: OverallState,
) -> Literal["collapse_summaries", "generate_final_summary"]:
    num_tokens = length_function(state["collapsed_summaries"])
    ## Collapse if it does not fit into the llm token context
    ## else we can do a final summary.
    if num_tokens > token_max:
        return "collapse_summaries"
    else:
        return "generate_final_summary"


# Here we will generate the final summary
async def generate_final_summary(state: OverallState):
    response = await _reduce(state["collapsed_summaries"])
    return {"final_summary": response}


if __name__ == "__main__":
    """Summary
    1. Load llm
    2. Load source
    3. Summarize the docs for stuf summarizing.
    4. For map reduce summary
        We create a langgraph to create sub summaries to the sub docs
        then we create a final summary from the sub summaries
        the reason we want to create sub summary is when our source data
        is larger than the llm's context window.

    """
    docs = load_source()
    more_split_docs = split_docs(docs)
    # stuff_summary(docs)

    # Construct the graph
    # Nodes:
    graph = StateGraph(OverallState)
    graph.add_node("generate_summary", generate_summary)
    graph.add_node("collect_summaries", collect_summaries)
    graph.add_node("collapse_summaries", collapse_summaries)
    graph.add_node("generate_final_summary", generate_final_summary)

    # Edges:
    ## map_summaries is the routing function
    ## that calls generate summary.
    ## it also the start of the graph
    graph.add_conditional_edges(START, map_summaries, ["generate_summary"])
    graph.add_edge("generate_summary", "collect_summaries")
    ## 'should_collapse' is the routing function
    ## that decies if token is within the limix of llm token context count
    ## then we should proceed to 'collapse_summaries'
    ## else we generate the final summary by calling the last stage
    ## 'generate_final_summary'
    graph.add_conditional_edges("collect_summaries", should_collapse)
    graph.add_conditional_edges("collapse_summaries", should_collapse)
    graph.add_edge("generate_final_summary", END)
    app = graph.compile()

    async def start():
        async for step in app.astream(
            {"contents": [doc.page_content for doc in more_split_docs]},
            {"recursion_limit": 10},
        ):
            print(list(step.keys()))

    asyncio.run(start())

    """Sample output
        ['generate_summary']
        ['generate_summary']
        ['generate_summary']
        ['generate_summary']
        ['generate_summary']
        ['generate_summary']
        ['generate_summary']
        ['generate_summary']
        ['generate_summary']
        ['generate_summary']
        ['generate_summary']
        ['generate_summary']
        ['generate_summary']
        ['generate_summary']
        ['collect_summaries']
        ['collapse_summaries']
        ['collapse_summaries']
        ['generate_final_summary']
    """
