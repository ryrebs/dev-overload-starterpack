from llama_index.core.workflow import (
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Context,
)
import random
from llama_index.utils.workflow import (
    draw_all_possible_flows,
    draw_most_recent_execution,
)
from llama_index.llms.openai import OpenAI

import asyncio
from llama_index.llms.ollama import Ollama


llm = Ollama(
    model="qwen3:8b",
    request_timeout=360.0,
    # Manually set the context window to limit memory usage
    context_window=8000,
)


class BasicOpenAIGenerator(Workflow):
    @step
    async def generate(self, ev: StartEvent) -> StopEvent:
        ## Use llm to get result
        response = await llm.acomplete(ev.query)
        return StopEvent(result=str(response))


class FailedEvent(Event):
    error: str

class InputEvent(Event):
    input_str: str


class SetupEvent(Event):
    error: bool


class QueryEvent(Event):
    query: str


class LoopWorkflow(Workflow):

    @step
    async def answer_query(
        self, ev: StartEvent | QueryEvent
    ) -> FailedEvent | StopEvent:
        value = ev.query
        rd = random.randint(0, 1)
        if rd == 0:
            return FailedEvent(error="Failed event")
        return StopEvent(
            result=f"Stop Success event got expected number {value} : {rd}"
        )

    @step
    async def improve_query(self, ev: FailedEvent) -> QueryEvent | StopEvent:
        rd = random.randint(0, 1)
        value = ev.error
        if rd == 0:
            return QueryEvent(query="Query event")
        return StopEvent(result=f"Stop Success event got expected number {value}: {rd}")


class WorkflowWithContext(Workflow):
    @step
    async def setup(self, ctx: Context, ev: StartEvent) -> StopEvent:
        if hasattr(ev, "data"):
            await ctx.store.set("data", ev.data)
        return StopEvent(result=None)

    @step
    async def query(self, ctx: Context, ev: StartEvent) -> StopEvent:
        if hasattr(ev, "query"):
            try:
                data = await ctx.store.get("data")
                return StopEvent(result=f"Got the data {data}")
            except:
                StopEvent(result="No data result")
        return None

class CollectExampleFlow(Workflow):
    @step
    async def setup(self, ev: StartEvent) -> SetupEvent:       
        print("I got set up")
        return SetupEvent(error=False)

    @step
    async def collect_input(self, ev: StartEvent) -> InputEvent:
        if hasattr(ev, "input_str"):
            # perhaps validate the input
            print("I got some input")
            return InputEvent(input_str=ev.input_str)

    @step
    async def parse_query(self, ev: StartEvent) -> QueryEvent:
        if hasattr(ev, "query"):
            # parse the query in some way
            print("I got a query")
            return QueryEvent(query=ev.query)

    @step
    async def run_query(
        self, ctx: Context, ev: InputEvent | SetupEvent | QueryEvent
    ) -> StopEvent | None:

        ## We define functions as  start events
        ## these functions execute and return  these events
        ready = ctx.collect_events(ev, [QueryEvent, InputEvent, SetupEvent])
        
        ## Each call to run_query decies wether to proceed
        if ready is None:
            print("Not enough events yet")
            return None

        # run the query
        print("Now I have all the events")
        print(ready)

        ## Here we got all the events 0,1,2 or [QueryEvent, InputEvent, SetupEvent]
        result = f"Ran query '{ready[0].query}' on input '{ready[1].input_str}'"
        return StopEvent(result=result)


async def main():
    # ##----- Basic start and stop flows
    # w = BasicOpenAIGenerator(timeout=600, verbose=False)
    # result = await w.run(query="What's LlamaIndex?")
    # print(result)

    # ##----- Example of building loop flows
    # w = LoopWorkflow(timeout=600, verbose=True)
    # result = await w.run(query="What's LlamaIndex?")
    # print(result)

    # ##----- Workflow with context
    # w = WorkflowWithContext(verbose=True)
    # ctx = Context(w)

    # ## Both start events definitions are ran
    # result = await w.run(query="Can I kick it?", ctx=ctx)
    # print(f"First run query result: {result}")

    # result = await w.run(data="Yes you can", ctx=ctx)
    # print(f"Second run step result {result}")

    # result = await w.run(query="Can I kick it?", ctx=ctx)
    # print(f"Third run step result {result}")

    ##----- Multiple events waiting
    w = CollectExampleFlow()
    result = await w.run(input_str="Here's some input", query="Here's my question")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
