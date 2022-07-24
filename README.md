# Description

This repo contains code that

- Deploys a MySQL server on a Kubernetes cluster
- Attaches a persistent volume to it, so the data remains contained if pods are restarting
- Deploys have 3 replicas Flask API to add, delete, modify, patch and put students (name, email, age, cellphone) in the MySQL database

## Kubernetes_homework


### Getting started

1. Clone the repository
2. Pull the mysql image from Dockerhub: Docker pull mysql:8

### Deployments

1. Add the secrets to your kubernetes cluster: kubectl apply -f ./Kubernetes/mysql-secret.yaml
2. Create the MySQL deployment: kubectl apply -f Kubernetes/mysql.yaml
3. Create the Flask API deployment: kubectl apply -f Kubernetes/flask-app.yaml
You can check the status of the pods, services and deployments.


This project is Genesis homework
