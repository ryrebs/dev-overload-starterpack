import getpass
import os

from langchain.chat_models import init_chat_model
from langchain_community.utilities import SQLDatabase
from typing_extensions import TypedDict, Annotated
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain.chains import create_sql_query_chain
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# Embedding model (Make sure ollama is runnning and llama3.2:1b is pulled)
embeddings = OllamaEmbeddings(model="codeqwen")


db = SQLDatabase.from_uri(
    f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_USER_PWD')}@localhost:5432/{os.environ.get('DB_NAME')}"
)


class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str


llm = init_chat_model("codeqwen", model_provider="ollama")


query_examples = [
    {"input": "List all tours.", "query": "SELECT * FROM tour_tour"},
    {
        "input": "Count of all active tours.",
        "query": "SELECT COUNT(*) FROM tour_tour where is_active=true",
    },
    {
        "input": "List of all booking itineraries.",
        "query": "SELECT * FROM tour_customerbookinitinerary",
    },
    {
        "input": "List of all custom tours or tour that are custom.",
        "query": "SELECT * FROM tour_customtour",
    },
]


class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]


def populate_store_with_examples():
    to_vectorize = [" ".join(example.values()) for example in query_examples]
    vector_store = Chroma.from_texts(
        to_vectorize,
        embeddings,
        metadatas=query_examples,
        collection_name="query_collection",
        persist_directory="./chroma_langchain_db",
    )

    return vector_store


def write_query(state: State):
    """Generate SQL query to fetch information."""

    ## You can use a prompt template from promp hub
    ## or compose your prompt manually

    prompt = f"""
    Given an input question, create a syntactically correct {db.dialect} to query to run to help find the answer.
    Unless the user specifies in his question a specific number of examples they wish to obtain,
    always limit your query to at most top 10 results.
    You can order the results by a relevant column to return the most interesting examples in the database.
    Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.

    Only use the following tables and columns:
    {db.table_info}

    Question: {state['question']}
    """
    llm = init_chat_model("mistral", model_provider="ollama")
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}


def write_query_with_few_shot(state: State):
    """Generate SQL query to fetch information with few shot examples."""

    ## Manually populate the store
    vector_store = populate_store_with_examples()

    ## Or automatically create the store
    # example_selector = SemanticSimilarityExampleSelector.from_examples(
    #     query_examples,
    #     OllamaEmbeddings(model="codeqwen"),
    #     vector_store,
    #     k=1,
    #     input_keys=["input"],
    # )

    example_selector = SemanticSimilarityExampleSelector(vectorstore=vector_store, k=3)
    example_prompt = PromptTemplate.from_template(
        "User input example: {input}\nSQL query: {query}"
    )
    prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix="""You're a sql expert. Unless the user specifies in his question a specific number of examples they wish to obtain,
            always limit your query to at most top {top_k} results.
            You can order the results by a relevant column to return the most interesting examples in the database.
            Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.
            Unless otherwise specificed, do not return more than {top_k} rows.

            Only use the following tables and columns:
            Here is the relevant table info: {table_info}
            Below are a number of examples of questions and their corresponding SQL queries.
            """,
        suffix="Actual user input: {input}\nSQL query: ",
        input_variables=["input", "top_k", "table_info"],
    )

    ## create_sql_query_chain provides necessary information
    ## to answer the query like: table_info, and max returning row (default 5)
    ## Automatically maps question to input, k to top_k, table_info to table_info
    ## on FewShotPromptTemplate
    chain = create_sql_query_chain(llm, db, prompt, k=3)
    result = chain.invoke({"question": state["question"]})
    return {"query": result}


def execute_query(state: State):
    """Execute SQL query."""
    execute_query_tool = QuerySQLDatabaseTool(db=db)
    return {"result": execute_query_tool.invoke(state["query"])}


def generate_answer(state: State):
    """Answer question using retrieved information as context."""
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )
    response = llm.invoke(prompt)
    return {"answer": response.content}


def init_graph():
    memory = MemorySaver()
    graph_builder = StateGraph(State).add_sequence(
        [write_query_with_few_shot, execute_query, generate_answer]
    )
    graph_builder.add_edge(START, "write_query_with_few_shot")
    graph = graph_builder.compile(
        checkpointer=memory, interrupt_before=["execute_query"]
    )

    return graph


def start(config, graph, question):

    for step in graph.stream(
        {"question": question},
        config,
        stream_mode="updates",
    ):
        print(step)

    ## Jumps out from the loop just before  'execute_query' runs.
    try:
        user_approval = input("Do you want to go to execute query? (yes/no): ")
    except Exception:
        user_approval = "no"

    if user_approval.lower() == "yes":
        ## If approved, continue the graph execution
        ## the graph knows where it left of, since
        ## we setup checkpointer
        for step in graph.stream(None, config, stream_mode="updates"):
            print(step)
    else:
        print("Operation cancelled by user.")


if __name__ == "__main__":
    """Summary
    0. Connect to a database (postgresql)
    1. Setup your LLM model
    2. Create the function that writes the query using llm
    3. Create the function that executes the query
    4. Create the final output by answering the user question and using the result from the query
    5. Add interupt. We want to interrupt the process before or after it executes.
    6. Added few shot example prompt, where we feed the llm few examples to based its query generation to improve its answers.
    7. We want to store our examples as embeddings , this way we can include only query related examples dynamically.
    """

    config = {"configurable": {"thread_id": "1"}}
    start(config, init_graph(), "How many custom tour are there?")
