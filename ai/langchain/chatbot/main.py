from typing import Annotated
import sqlite3

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command, interrupt
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import ToolMessage


## Setup persistence
conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
memory = SqliteSaver(conn)
config = {"configurable": {"thread_id": "1"}}


# The schema of the graph
class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]  # Reducer function (Add)

    # Customizing the state
    name: str
    birthday: str


@tool
# Note that because we are generating a ToolMessage for a state update, we
# generally require the ID of the corresponding tool call. We can use
# LangChain's InjectedToolCallId to signal that this argument should not
# be revealed to the model in the tool's schema.
def human_assistance(
    name: str, birthday: str, tool_call_id: Annotated[str, InjectedToolCallId]
):
    """Request assistance from a human."""

    ## >> Interrupts exits the execution flow << ##
    human_response = interrupt(
        {
            "question": "Is this correct?",
            "name": name,
            "birthday": birthday,
        },
    )

    ## If the information is correct, update the state as-is.
    if human_response.get("correct", "").lower().startswith("y"):
        verified_name = name
        verified_birthday = birthday
        response = "Correct"
    ## Otherwise, receive information from the human reviewer.
    else:
        verified_name = human_response.get("name", name)
        verified_birthday = human_response.get("birthday", birthday)
        response = f"Made a correction: {human_response}"

    ## This time we explicitly update the state with a ToolMessage inside
    ## the tool.
    state_update = {
        "name": verified_name,  # state key/value
        "birthday": verified_birthday,  #  state key/value
        ## Since this a tool call, we set the tool call's response
        "messages": [ToolMessage(response, tool_call_id=tool_call_id)],
    }

    ## We return a Command object in the tool to update our state.
    return Command(update=state_update)


@tool(response_format="content")
def search_info(query: str):
    """Retrieve any search demo data"""

    ## This is just a dummy tool for demo
    # return "Tool was called."

    ## Demo for birthday and name search
    return "Birthday April 4 2025, name is LangGraph"


llm = init_chat_model(model="qwen2.5:7b", model_provider="ollama")
llm_with_tools = llm.bind_tools([search_info, human_assistance])


def chatbot(state: State):
    # Because we will be interrupting during tool execution,
    # we disable parallel tool calling to avoid repeating any
    # tool invocations when we resume.
    message = llm_with_tools.invoke(state["messages"])
    assert len(message.tool_calls) <= 1
    return {"messages": [message]}


def stream_graph_updates(user_input: str):
    for event in graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config=config,
        stream_mode="values",
    ):
        event["messages"][-1].pretty_print()


## Helper function to demonstrate checkpoint, tool calling and interrupt flow
def start_flow_lesson_1(graph):
    user_input = "I need some expert guidance for building an AI agent. Could you request assistance for me?"
    config = {"configurable": {"thread_id": "1"}}

    ## This will call our human assistance function
    ## and stop at the tool call
    events = graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode="values",
    )
    for event in events:
        print(event)
        if "messages" in event:
            event["messages"][-1].pretty_print()

    ## This will resume the tool call and pass
    ## response as a result of the tool call
    ## Thus the result from the human assistance is the user or human's input.
    human_response = (
        "We, the experts are here to help! We'd recommend you check out LangGraph to build your agent."
        "It's much more reliable and extensible than simple autonomous agents."
    )
    human_command = Command(resume={"data": human_response})

    events = graph.stream(human_command, config, stream_mode="values")
    for event in events:
        if "messages" in event:
            event["messages"][-1].pretty_print()


## Helper function to demonstrate checkpoint, tool calling, interrupt flow
## and updating the state
def start_flow_lesson_2(graph):
    ## Updating the state
    user_input = (
        "Can you look up when LangGraph was released? "
        "When you have the answer, use the human_assistance tool for review."
    )
    config = {"configurable": {"thread_id": "1"}}

    events = graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode="values",
    )
    for event in events:
        if "messages" in event:
            event["messages"][-1].pretty_print()

    ## We will resume the execution flow after the interrupt hits ##
    ## We'll provide the value for resume

    ## Here we explicitly set the values
    ## We can also use input() to get
    ## the value from the user
    ## but for demo purpose we'll set like this.
    human_command = Command(
        resume={
            "name": "LangGraph",
            "birthday": "Jan 17, 2024",
        },
    )

    ## Knows at which process or stage to resume
    events = graph.stream(human_command, config, stream_mode="values")
    for event in events:
        if "messages" in event:
            event["messages"][-1].pretty_print()


if __name__ == "__main__":
    # Add tool nodes
    tools = ToolNode([search_info, human_assistance])

    # Define schema/state
    graph_builder = StateGraph(State)

    # Add nodes
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_node("tools", tools)

    # Add edges
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge("chatbot", END)

    graph_builder.add_conditional_edges(
        "chatbot",  # chatbot will be the 'source', it tells you if chatbot ask to use a tool
        tools_condition,  # Router; Returns a tool node
        # The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node
        # It defaults to the identity function, but if you
        # want to use a node named something else apart from "tools",
        # You can update the value of the dictionary to something else
        # e.g., "tools": "my_tools"
        {"tools": "tools", END: END},  # Path mappings;Go to tools if exists else END
    )

    ## Remember previous chat history using sqlite
    # graph = graph_builder.compile(checkpointer=memory)

    ## Using memory
    graph = graph_builder.compile(checkpointer=MemorySaver())

    ## start_flow_lesson_1(graph)
    start_flow_lesson_2(graph)
