#!/bin/bash

# k create namespace cattle-system
# k create secret tls rancher.topfilms.io-tls --cert=cert.pem --key=key.pem -n cattle-system
# helm repo add rancher-latest https://releases.rancher.com/server-charts/latest
# helm repo update
helm install rancher rancher-latest/rancher -f values.yaml -n cattle-system