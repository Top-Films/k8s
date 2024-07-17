#!/bin/bash

# helm repo add jenkins https://charts.jenkins.io
helm uninstall jenkins -n jenkins
kubectl delete pv jenkins
kubectl delete sc jenkins
kubectl delete sa jenkins -n jenkins
kubectl delete clusterrole jenkins
kubectl delete clusterrolebinding jenkins
# kubectl delete secret jenkins.topfilms.io-tls -n jenkins