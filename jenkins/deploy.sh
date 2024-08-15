#!/bin/bash

# k create namespace keycloak
# kubectl create secret tls jenkins.topfilms.io-tls --cert=cert.pem --key=key.pem -n jenkins
# kubectl apply -f storage.yaml -n jenkins
# kubectl apply -f sa.yaml -n jenkins
helm repo add jenkins https://charts.jenkins.io
helm repo update
helm upgrade jenkins jenkinsci/jenkins -f values-with-secrets.yaml --install --atomic --debug --history-max=3 --namespace jenkins