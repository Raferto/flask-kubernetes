# Deploying a Flask API and MySQL server on Kubernetes

This repo contains code that 
1) Deploys a MySQL server on a Kubernetes cluster
2) Attaches a persistent volume to it, so the data remains contained if pods are restarting
3) Deploys a Flask API to add, delete and modify users in the MySQL database

## Prerequisites
1. Have `Docker` and the `Kubernetes CLI` (`kubectl`) installed together with `Minikube` (https://kubernetes.io/docs/tasks/tools/)

## Getting started
1. Clone the repository
2. Configure `Docker` to use the `Docker daemon` in your kubernetes cluster via your terminal: `eval $(minikube docker-env)`
3. Pull the latest mysql image from `Dockerhub`: `Docker pull mysql`
4. Build a kubernetes-api image with the Dockerfile in this repo: `Docker build -t flask-api .`

## Secrets
`Kubernetes Secrets` can store and manage sensitive information. For this example we will define a password for the
`root` user of the `MySQL` server using the `Opaque` secret type. For more info: https://kubernetes.io/docs/concepts/configuration/secret/

1. Encode your password in your terminal: `echo -n admin123 | base64`
2. Add the output to the `flaskapi-secrets.yml` file at the `db_root_password` field

## Deployments
Get the secrets, persistent volume in place and apply the deployments for the `MySQL` database and `Flask API`

1. Add the secrets to your `kubernetes cluster`: `kubectl apply -f flaskapi-secrets.yml`
2. Create the `persistent volume` and `persistent volume claim` for the database: `kubectl apply -f mysql-pv.yml`
3. Create the `MySQL` deployment: `kubectl apply -f mysql-deployment.yml`
4. Create the `Flask API` deployment: `kubectl apply -f flaskapp-deployment.yml`

You can check the status of the pods, services and deployments.

## Creating database and schema
The API can only be used if the proper database and schemas are set. This can be done via the terminal.
1. Connect to your `MySQL database` by setting up a temporary pod as a `mysql-client`: 
   `kubectl run -it --rm --image=mysql --restart=Never mysql-client -- mysql --host mysql --user=root --password=admin123`
   make sure to enter the (decoded) password specified in the `flaskapi-secrets.yml`
2. Create the database and table
   1. `CREATE DATABASE phonebook;`
    2. `USE phonebook;`
    3. ```
    CREATE TABLE `phonebook` (
      `id` varchar(50) NOT NULL,
      `nama` varchar(50) NOT NULL,
      `alamat` text NOT NULL,
      `notelp` varchar(50) NOT NULL,
      `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
      `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      PRIMARY KEY (`id`)
    );
    ```
    
## Expose the API
The API can be accessed by exposing it using minikube: `minikube service flask-service`. This will return a `URL`. If you paste this to your browser you will see the `hello world` message. You can use this `service_URL` to make requests to the `API`
