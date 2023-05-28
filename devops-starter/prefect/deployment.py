from flow import my_flow
from prefect.deployments import Deployment


deployment = Deployment.build_from_flow(
    flow=my_flow, # Flow name
    name="my-flow-dep", # Deployment name
    parameters={"url": "https://catfact.ninja/fact/"},
    work_queue_name="my-work-pool"
)

if __name__ == "__main__":
    deployment.apply()