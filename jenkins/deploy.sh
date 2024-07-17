#!/bin/bash

# helm repo add jenkins https://charts.jenkins.io
# kubectl create secret tls jenkins.topfilms.io-tls --cert=cert.pem --key=key.pem -n jenkins
kubectl apply -f storage.yaml -n jenkins
kubectl apply -f sa.yaml -n jenkins
helm install jenkins -n jenkins -f values-with-secrets.yaml jenkinsci/jenkins