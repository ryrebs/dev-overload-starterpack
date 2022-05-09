### Install kubectl
    curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl

### Make the binary executable

    chmod +x ./kubectl

### Move binary to PATH
    
    sudo mv ./kubectl /usr/local/bin/kubectl

### Enable shell completion when using oh-my-zsh
### Update this line on ~/.zshrc

    plugins=(kubectl) 


### Install minikube
### Make executable and move to path in one line:

    curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.28.2/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/

### Create the local cluster

    minikube start

### Set minikube context

    kubectl config use-context minikube

### Run the dashboard

    minikube dashboard

### For this setup, use the minikube Docker daemon
### so images are available locally, instead of pushing
### the images to a registry

    eval $(minikube docker-env)

### Disable the minikube Docker daemon
    
    eval $(minikube docker-env -u)

### **TERMS**
*Minikube* is a lightweight Kubernetes implementation that creates a VM on your local machine and deploys a simple cluster containing only one node.  [Source](https://kubernetes.io/docs/tutorials/kubernetes-basics/create-cluster/cluster-intro/)

a. *Kubernetes Pod* is a group of one or more Containers, tied together for the purposes of administration and networking. 

b. *Kubernetes Deployment* checks on the health of your Pod and restarts the Pod’s Container if it terminates. Deployments are the recommended way to manage the creation and scaling of Pods.

c. *Service* handles the request.

d. *Node* a kubelet, runs pods and communicates with master, worker machine

e. *Cluster* a collection of nodes

### Create a deployment that manages a Pod (Imperative)

    kubectl run hello-node --image=hello-node:v1 --port=8080 --image-pull-policy=Never

    --image-pull-policy is set to false since we don't need to pull the image from a registry.

### View the deployment/s

    kubectl get deployments

### Delete Deployment (imperatively created)

    kubectl delete deployment/<DEPLOYMENT_NAME>

### Delete Deployment (declaratively created)

    kubectl delete -f <file_path>.yaml

###  View the pod

    kubectl get pods

### View cluster events:

    kubectl get events

### View the kubectl configuration:

    kubectl config view

### Create a service to expose the Pod as a kubernetes service
### since the pod is accesible only via its internal IP within
### the Kubernetes cluster

    kubectl expose deployment hello-node --type=LoadBalancer

### View the Service 

    kubectl get services

### Start the service

    minikube service hello-node

## Get minikube ip

    minikube ip

### Clean up commands:

    kubectl delete service hello-node
    kubectl delete deployment hello-node

### Remove docker images:

    docker rmi hello-node:v1 hello-node:v2 -f

### Stop minikube vm

    minikube stop
    eval $(minikube docker-env -u)

### Deleting the vm

    minikube delete

### UPDATING app flow:

    docker build -t hello-node:v2 .

    kubectl set image deployment/hello-node hello-node=hello-node:v2

    minikube service hello-node

##### Original tutorial source: https://kubernetes.io/docs/tutorials/hello-minikube/


