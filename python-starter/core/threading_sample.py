"""
    Thread or Thread of execution is a set of instructions that need to be executed.
    Resides under a Process, each threads can share resource from other threads.
    Threads are usually use for I/O bound task, to avoid an idle CPU and blocking
    a main thread.    

    Notes: 
        - Os threads vs CPU threads (virtual cores)

        - Concurrency:  Executing tasks simultaneously by either:
                            - Multi-threading:      Multiple threads is used when you want to divide a set of instructions into 
                                                    another threads to achieve concurrency.
                                                    Preemptive scheduling(schedule an instruction for later execution) that is managed by the OS.
                            
                            - Asynchronous:        (Single threaded) In python, executing tasks  happens by cooperative scheduling. The instructions/code tells
                                                    the OS when to pause an execution and give way to another instructions.            
                            
                            - Multi-processing:     Multiple instance of an application that executes at the same time and contains one or more threads.
                                                    Limited to no. of cores and is usually use for CPU bound tasks.    
                                                    
                            - Parallelism:          Multi-processing denotes parallelism which - tasks executes at the same time.                                                        
"""

from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed

import logging

logging.basicConfig(filename="err.log", level=logging.DEBUG)


def p(q):
    if q == 7:
        logging.info("Raise 7")
        return None
    return q * 2


## Create max 10 threads
with ThreadPoolExecutor(10) as executor:
    ## Create and execute futures
    # executor.map(p, [n for n in range(1000)])

    ## Create list of futures
    futures = [executor.submit(p, i) for i in range(10)]
    for future in as_completed(futures):
        print("res::", future.result())

## See also multiprocessing, ProcessPoolExecutor
