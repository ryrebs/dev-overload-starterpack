"""
    What is a coroutine?
        Coroutine is a just like a simple function that can pause to allow other block of codes or
        another function to execute then resume its execution once the other block of codes is done.        

    Examples are taken from:
        From https://docs.python.org/3/library/asyncio-task.html    

"""

import asyncio
import time

## To make a function asynchronous
## async keyword is required at the start
## of the function

## Waiting for other function to finish
## then execute back the remaining lines of code
async def get_len_what(delay, what):
    print("Created:: ", time.strftime("%X"))
    ## wait for this function to finish
    ## this asyncio sleep function
    ## will pause for delay duration
    ## and pass back control to event loop
    t = 0
    for i in range(len(what)):
        await asyncio.sleep(delay)
        print(what)
        t = t + i
    return t


## main will serve as the main entry point
async def main1():
    start = time.time()
    print("Main one started at", start)

    ## await this function
    ## simply executing this function
    hello = await get_len_what(5, "hello")
    world = await get_len_what(0, "world now")

    end = time.time()
    print("Finished at", end)
    print(f"Diff {int(end-start)}")


async def main2():
    ## Couroutines are created at same time
    task1 = asyncio.create_task(get_len_what(1, "hello"))
    task2 = asyncio.create_task(get_len_what(2, "world"))

    start = time.time()
    print("Main two started at", start)

    ## Coroutines must be awaited in order to be executed
    ## await tells the event loop that there are other coroutine
    ## needed to be executed

    ## Awaiting 1 by 1
    await task1
    await task2

    ## Awaiting list of futures using asyncio.wait
    # done, pending = await asyncio.wait([task1, task2])

    ## Awaiting list of futures using asyncio.gather
    # result = await asyncio.gather(*[task1, task2])

    end = time.time()
    print("Finished at", end)
    print(f"Time Diff {int(end-start)}")


def main_one():
    asyncio.run(main1())  ## run the event loop


def main_two():
    asyncio.run(main2())  ## run the event loop


if __name__ == "__main__":
    ## Non Coroutine
    ## N Delay blocks the execution of another async function
    """
    Main one started at 1648723363.7157466
    Created::  18:42:43
    hello
    hello
    hello
    hello
    hello
    Created::  18:43:08
    world now
    world now
    world now
    world now
    world now
    world now
    world now
    world now
    world now
    Finished at 1648723388.7406456
    Time Diff 25
    """
    # main_one()

    ## Coroutine
    ## N Delay does not block but moves to another async function which is a coroutine
    """
        Main two started at 1648723493.605758
        Created::  18:44:53
        Created::  18:44:53
        hello
        world
        hello
        hello
        world
        hello
        hello
        world
        world
        world
        Finished at 1648723503.6144292
        Time Diff 10
    """
    # main_two()
