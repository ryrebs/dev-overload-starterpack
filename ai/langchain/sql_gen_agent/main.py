from langchain_community.utilities import SQLDatabase
from typing import Any

from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda, RunnableWithFallbacks
from langgraph.prebuilt import ToolNode
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate

from typing import Annotated, Literal

from langchain_core.messages import AIMessage

from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import AnyMessage, add_messages

model = "qwen2.5:7b"


# Define the state for the agent
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


# Describe a tool to represent the end state
class SubmitFinalAnswer(BaseModel):
    """Submit the final answer to the user based on the query results."""

    final_answer: str = Field(..., description="The final answer to the user")


query_check_system = """You are a SQL expert with a strong attention to detail.
Double check the SQLite query for common mistakes, including:
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins
- Correct use of aliases

If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.

You will call the appropriate tool to execute the query after running this check."""

# Add a node for a model to generate a query based on the question and schema
query_gen_system = """You are a SQL expert with a strong attention to detail.

Given an input question, output a syntactically correct SQLite query to run, then look at the results of the query and return the answer.

DO NOT call any tool besides SubmitFinalAnswer to submit the final answer.

When generating the query:

Output the SQL query that answers the input question without a tool call.

Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.

If you get an error while executing a query, rewrite the query and try again.

If you get an empty result set, you should try to rewrite the query to get a non-empty result set. 
NEVER make stuff up if you don't have enough information to answer the query... just say you don't have enough information.

If you have enough information to answer the input question, simply invoke the appropriate tool to submit the final answer to the user.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database."""


@tool
def db_query_tool(query: str) -> str:
    """
    Execute a SQL query against the database and get back the result.
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    """
    result = db.run_no_throw(query)
    if not result:
        return "Error: Query failed. Please rewrite your query and try again."
    return result


db = SQLDatabase.from_uri("sqlite:///Chinook.db")
llm = init_chat_model(model, model_provider="ollama")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()

## Prebuilt tool for sql in SQLDatabaseToolkit
list_tables_tool = next(tool for tool in tools if tool.name == "sql_db_list_tables")
get_schema_tool = next(tool for tool in tools if tool.name == "sql_db_schema")

## Query check llm tool
query_check_prompt = ChatPromptTemplate.from_messages(
    [("system", query_check_system), ("placeholder", "{messages}")]
)
query_check = query_check_prompt | llm.bind_tools(
    [db_query_tool], tool_choice="required"
)

## Query generation llm tool
query_gen_prompt = ChatPromptTemplate.from_messages(
    [("system", query_gen_system), ("placeholder", "{messages}")]
)
query_gen = query_gen_prompt | llm.bind_tools([SubmitFinalAnswer])


## Tool error handlng
def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    print("error: ", state["messages"][-1])
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }


## Explicit tool call, we want to list the tables
def first_tool_call(state: State) -> dict[str, list[AIMessage]]:
    return {
        "messages": [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "sql_db_list_tables",
                        "args": {},
                        "id": "tool_abcd123",
                    }
                ],
            )
        ]
    }


## Add error handling to tools
def create_tool_node_with_fallback(tools: list) -> RunnableWithFallbacks[Any, dict]:
    """
    Create a ToolNode with a fallback to handle errors and surface them to the agent.
    """
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )


def model_check_query(state: State) -> dict[str, list[AIMessage]]:

    # Check query
    message = query_check.invoke({"messages": [state["messages"][-1]]})
    """
    Use this tool to double-check if your query is correct before executing it.
    """
    return {"messages": [message]}


def query_gen_node(state: State):
    # Generate the query
    message = query_gen.invoke(state)

    # Sometimes, the LLM will hallucinate and call the wrong tool. We need to catch this and return an error message.
    tool_messages = []
    if message.tool_calls:
        for tc in message.tool_calls:
            if tc["name"] != "SubmitFinalAnswer":
                tool_messages.append(
                    ToolMessage(
                        content=f"Error: The wrong tool was called: {tc['name']}. Please fix your mistakes. Remember to only call SubmitFinalAnswer to submit the final answer. Generated queries should be outputted WITHOUT a tool call.",
                        tool_call_id=tc["id"],
                    )
                )
    else:
        tool_messages = []
    return {"messages": [message] + tool_messages}


# Define a conditional edge to decide whether to continue or end the workflow
def should_continue(
    state: State,
) -> Literal[END, "model_check_query", "query_gen_node"]:
    messages = state["messages"]
    last_message = messages[-1]
    ## If there is a tool call, then we finish
    ##  A tool call from query_gen_node
    if getattr(last_message, "tool_calls", None):
        return END
    if last_message.content.startswith("Error:"):
        ## If error generate again
        return "query_gen_node"
    else:
        ## If ok proceed to query validation
        return "model_check_query"


if __name__ == "__main__":
    # Define a new graph
    workflow = StateGraph(State)

    # Nodes for getting info from db
    workflow.add_node("first_tool_call", first_tool_call)

    workflow.add_node(
        "list_tables_tool", create_tool_node_with_fallback([list_tables_tool])
    )

    workflow.add_node(
        "get_schema_tool", create_tool_node_with_fallback([get_schema_tool])
    )

    # Node for schema tool
    model_get_schema = llm.bind_tools([get_schema_tool])

    def model_get_schema_tool(state: State):
        message = [model_get_schema.invoke(state["messages"])]
        return {"messages": message}

    workflow.add_node("model_get_schema", model_get_schema_tool)

    # Node for query generation
    workflow.add_node("query_gen_node", query_gen_node)

    # Node for query correction
    workflow.add_node("model_check_query", model_check_query)

    # Node executing the query
    workflow.add_node("execute_query", create_tool_node_with_fallback([db_query_tool]))

    # Specify the edges between the nodes

    workflow.add_edge(START, "first_tool_call")
    workflow.add_edge("first_tool_call", "list_tables_tool")
    workflow.add_edge("list_tables_tool", "model_get_schema")
    workflow.add_edge("model_get_schema", "get_schema_tool")
    workflow.add_edge("get_schema_tool", "query_gen_node")
    workflow.add_conditional_edges(
        "query_gen_node",
        should_continue,
    )
    workflow.add_edge("model_check_query", "execute_query")
    workflow.add_edge("execute_query", "query_gen_node")

    # Compile the workflow into a runnable
    app = workflow.compile()

    # Run the agent
    for event in app.stream(
        {
            "messages": [
                (
                    "user",
                    ## Simple questions for demo and small param LLMs
                    "How many sales agent are there?Make sure you get the schema of the database and the list of tables before answering.",
                )
            ],
        },
        stream_mode="values",
        config={"recursion_limit": 100},
    ):
        print(event["messages"][-1].pretty_print())

    """ SUMMARY
    1. Setup llm and states
    2. Use already built tools for SQL (SQLDatabaseToolkit)
    3. Setup error handling to retry invalid queries

    Graph overview:
    
    first_tool_call (calls tool list tables) -> list table -> get schema -> generate query

    -> check query -> execute query -> if error;generate_query -> goto check query (cycle until correct query is generated)
    
    -> ouput final state -> END

    ## FINAL ANSWER:
    ================================== Ai Message ==================================
    Tool Calls:
    SubmitFinalAnswer (ae168116-8734-4ba2-be99-2c055c4a0ea8)
    Call ID: ae168116-8734-4ba2-be99-2c055c4a0ea8
    Args:
        final_answer: There are 3 sales agents in the database.

    ## Note the better the llm the better it decides whether to use a tool.
    """
