## Prefect getting started setup and lessons

---

### Setup

- `pipenv install`

- Test a sample prefect flow:

  `pipenv python run flow.py`

### Deployment using yaml configurations.

- Export the prefect api url env variable:

        export PREFECT_API_URL=http://<prefect-ip>/api

- Build a basic deployment configuration file:

       prefect deployment build ./<python-file>:<entrypoint-flow-function> -n <deployment-name> -q <work-pool>

- Modify the file output `*-deployment.yaml` generated from the previous command as necessary.

- Apply the deployment on the prefect server.

        prefect deployment apply <deployment-file | *-deployment.yaml>

- Run the default agent to accept jobs at \<work-queue\>.

        prefect agent start -q <work-queue>

- Or create a pool with type _Process_ (default) and create a work queue (Default queue is also created.). Then run the process and queue with:

        prefect worker start --pool <pool-name> --work-queue <default|manually-created-custom-queue-name->

- Run the flow

        prefect deployment run '<flow-name>/<deployment-name>'

### Deployment with python file.

- See/update `deployment.py`.

- Run with `python deployment.py`

### Setting up project structure with `prefect project` using _local_ recipe.

- Create/Navigate to _prefect_project_setup_sample_ folder.

- Initialize the project with `prefect init project --recipe local`

- Update the necessary fileds on _deployment.yaml_ or _prefect.yaml_

- Deploy a deployment with `prefect deploy --name <deployment-name>`

- Deploy all deployments with `prefect deploy --all`
