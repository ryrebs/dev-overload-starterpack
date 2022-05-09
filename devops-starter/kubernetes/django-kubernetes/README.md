#### Quickstart,  run these commands make sure minikube and kubectl are installed
    minikube start
    kubectl config current-context
    eval $(minikube docker-env)
    minikube dashboard

#### Create the Dockerfile

#### Build the image

    docker build -t django-k8s:v1 .

#### Create the deployment

    kubectl run <deployment-name> --image=<IMAGE-NAME> --port=8000

    kubectl run django-k8s-deployment --image=django-k8s:v1 --port=8000

#### Or create declaratively

    kubectl apply -f django-deployment.yaml

#### Create the service

    kubectl apply -f django-service.yaml

### get and run the service

    kubectl get svc
    minikube service <deployment-name>

### Create a persistent volume

    touch volume.yaml
    kubectl apply -f volume.yaml

### Show persistent volume

    kubectl get pv

### Create persistent volume claim
### this a request that we want to use a storage

    touch persistent_volume_claim.yaml
    kubectl apply -f persistent_volume_claim.yaml

### Show pvc

    kubectl get pvc

### Create credentials
### using Kubernetes Secret object

    touch postgres_secret.yaml

#### Generate encoding

    echo -n <any string> | base64

#### Replace user and password field with the generated string

### Apply the secret

    kubectl apply -f postgres_secret.yaml

### Create the deployment for the postgres container

    touch postgres_deployment.yaml

### Apply the deployment

    kubectl apply -f postgres_deployment.yaml

### Create the service for postgres

    touch postgres_service.yaml

### Apply the service

    kubectl apply -f postgres_service.yaml

### Create a Job object for migration and apply

    touch  django-migration.yaml

### Run migration via cli

    kubectl exec <pod_name> -- python /app/manage.py migrate

### Check pods for completion , check the migration

    kubectl get pods --show-all
    kubectl logs django-migrations-wzjjk

#### *Credits to original tutorial* [here](https://medium.com/@markgituma/kubernetes-local-to-production-with-django-2-docker-and-minikube-ba843d85881)