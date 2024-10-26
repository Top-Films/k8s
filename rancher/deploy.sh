#!/bin/bash

export CA_CERT_PATH=""
export CA_CERT_PRIVATE_KEY_PATH=""

if [[ -z "$CA_CERT_PATH" || -z "$CA_CERT_PRIVATE_KEY_PATH" ]]; then
	echo "ERROR: Environment variables not set"
	exit 1
fi

set -x

cp $CA_CERT_PATH .
cp $CA_CERT_PRIVATE_KEY_PATH .

kubectl delete secret rancher.topfilms.io-tls --namespace cattle-system
kubectl create secret tls rancher.topfilms.io-tls --cert=cert.pem --key=key.pem --namespace cattle-system

rm cert.pem
rm key.pem

helm repo add rancher-latest https://releases.rancher.com/server-charts/latest
helm repo update

helm install rancher rancher-latest/rancher --values values.yaml --namespace cattle-system