import getpass
import os

from langchain.chat_models import init_chat_model
from langchain_community.utilities import SQLDatabase
from typing_extensions import TypedDict, Annotated
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langgraph.graph import START, StateGraph


db = SQLDatabase.from_uri(
    f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_USER_PWD')}@localhost:5432/{os.environ.get('DB_NAME')}"
)


class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str


llm = init_chat_model("codeqwen", model_provider="ollama")


class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]


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


if __name__ == "__main__":
    """Summary
    0. Connect to a database (postgresql)
    1. Setup your LLM model
    2. Create the function that writes the query using llm
    3. Create the function that executes the query
    4. Create the final output by answering the user question and using the result from the query
    """

    graph_builder = StateGraph(State).add_sequence(
        [write_query, execute_query, generate_answer]
    )
    graph_builder.add_edge(START, "write_query")
    graph = graph_builder.compile()

    for step in graph.stream(
        {"question": "How many tours are there?"}, stream_mode="updates"
    ):
        print(step)
