#!/bin/bash

# kubectl create secret tls auth.topfilms.io-tls --cert=cert.pem --key=key.pem -n keycloak
# kubectl apply -f secret.yaml -n keycloak
kubectl apply -f keycloak.yaml -n keycloak