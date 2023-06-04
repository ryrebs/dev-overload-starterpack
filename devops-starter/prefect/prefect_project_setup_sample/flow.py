import requests
from prefect import flow, task
from prefect.tasks import task_input_hash
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures import as_completed


## Cache the input, returning same result everytime
@task(retries=2, retry_delay_seconds=60, cache_key_fn=task_input_hash)
def call_api(url):
    response = requests.get(url)
    print(response.status_code)
    return response.json()


@task(name="task 1")
def t1():
    print('t1')

@task(name="task 2")
def t2():
    print('t2')


def t3(n):
    return n * 10

@flow(
    name="Flow dev app",
    version="dev_01")
def my_flow(url):
    """
    Docstring as flow description.
    """
    ## Cached input
    resp = call_api(url)
    print(resp)

    ## Concurrent execution is used by Task runner by default.
    t1.submit()
    t2.submit()

    ## Blocking task
    t1()

    ## Explicit concurrent execution
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = [pool.submit(t3, n) for n in [1,2,3]]

        for f in as_completed(futures):
            r = f.result()
            print(r)
        
    ## Subflow
    my_flow_2()


@flow
def my_flow_2():
    print("my_flow_2")

if __name__ == "__main__":
    my_flow("https://catfact.ninja/fact/")