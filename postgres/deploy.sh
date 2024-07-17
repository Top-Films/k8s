#!/bin/bash

kubectl apply -f secret.yaml -n postgres
kubectl apply -f storage.yaml -n postgres
helm install db oci://registry-1.docker.io/bitnamicharts/postgresql --namespace postgres -f values.yaml