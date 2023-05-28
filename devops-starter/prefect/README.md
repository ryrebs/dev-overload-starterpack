## Prefect getting started setup and lessons

---

### Setup

- `pipenv install`

- Test a sample prefect flow:

  `pipenv python run flow.py`

### Deployment using yaml configurations.

- Build a basic deployment configuration file:

       prefect deployment build ./<python-file>:<entrypoint-flow-function> -n <deployment-name> -q <work-pool>

- Modify the file output `*-deployment.yaml` generated from the previous command as necessary.

- Apply the deployment on the prefect server.

        prefect deployment apply <deployment-file | *-deployment.yaml>

- Run a worker agent to accept jobs at <work-pool>.

        prefect agent start -q <work-pool>

- Run the flow

        prefect deployment run '<flow-name>/<deployment-name>'

### Deployment with python file.

- See/update `deployment.py`.

- Run with `python deployment.py`
