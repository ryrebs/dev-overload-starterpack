from typing import Optional

from pydantic import BaseModel, Field
from typing import Optional

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from typing import List, Optional
from langchain_core.utils.function_calling import tool_example_to_messages


## When we extract data from a source this is how
## we want the data to look like.
class Person(BaseModel):
    """Information about a person."""

    # ^ Doc-string for the entity Person.
    # This doc-string is sent to the LLM as the description of the schema Person,
    # and it can help to improve extraction results.

    # Note that:
    # 1. Each field is an `optional` -- this allows the model to decline to extract it!
    # 2. Each field has a `description` -- this description is used by the LLM.
    # Having a good description can help improve extraction results.
    name: Optional[str] = Field(default=None, description="The name of the person")
    hair_color: Optional[str] = Field(
        default=None, description="The color of the person's hair if known"
    )
    height_in_meters: Optional[str] = Field(
        default=None, description="Height measured in meters"
    )


# Define a custom prompt to provide instructions and any additional context.
# 1) You can add examples into the prompt template to improve extraction quality
# 2) Introduce additional parameters to take context into account (e.g., include metadata
#    about the document from which the text was extracted.)
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "Convert units in to expected unit of measurement if necessary."  ## <- I'm using a weak model. It does not convert automatically
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value.",
        ),
        # Please see the how-to about improving performance with
        # reference examples.
        # MessagesPlaceholder('examples'),
        ("human", "{text}"),
    ]
)


## Model nesting
class Data(BaseModel):
    """Extracted data about people."""

    # Creates a model so that we can extract multiple entities.
    people: List[Person]


if __name__ == "__main__":
    llm = init_chat_model(model="mistral", model_provider="ollama")
    structured_llm = llm.with_structured_output(schema=Person)

    ## Note: The accuracy of the extraction depends on the model.
    ## update your prompt if the result is wrong.

    text_height_and_hair_color = "Alan Smith is 6 feet tall and has blond hair."
    prompt = prompt_template.invoke({"text": text_height_and_hair_color})
    res = structured_llm.invoke(prompt)
    print(res)

    text_with_name_only = "Alan Smith is the person"
    prompt = prompt_template.invoke({"text": text_with_name_only})
    res = structured_llm.invoke(prompt)
    print(res)

    structured_llm = llm.with_structured_output(schema=Data)
    text_with_multiple_persons = "My name is Jeff, my hair is black and i am 6 feet tall. Anna has the same color hair as me."
    prompt = prompt_template.invoke({"text": text_with_multiple_persons})
    res = structured_llm.invoke(prompt)
    print(res)

    ## Adding few shot examples.
    ## These are examples we feed to the llm to improve its extraction.

    examples = [
        (
            "The ocean is vast and blue. It's more than 20,000 feet deep.",
            Data(people=[]),
        ),
        (
            "Fiona traveled far from France to Spain.",
            Data(people=[Person(name="Fiona", height_in_meters=None, hair_color=None)]),
        ),
    ]

    messages = []

    ## "Structured output often uses tool calling under-the-hood"
    for txt, tool_call in examples:
        if tool_call.people:
            ai_response = "Detected people."
        else:
            ai_response = "Detected no people."

        ## ai_response is for the final message, and is optional for some providers
        messages.extend(
            tool_example_to_messages(txt, [tool_call], ai_response=ai_response)
        )

    message_no_extraction = {
        "role": "user",
        "content": "The solar system is large, but earth has only 1 moon.",
    }

    structured_llm = llm.with_structured_output(schema=Data)
    res = structured_llm.invoke([message_no_extraction])
    print(res)  ## Prints data with user

    res = structured_llm.invoke(messages + [message_no_extraction])
    print(res)  ## Prints data with NO user
