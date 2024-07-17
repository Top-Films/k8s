#!/bin/bash

kubectl delete deploy keycloak -n keycloak
kubectl delete svc keycloak -n keycloak
kubectl delete ing keycloak -n keycloak
kubectl delete secret keycloak-credentials -n keycloak
# kubectl delete secret auth.topfilms.io-tls -n keycloak