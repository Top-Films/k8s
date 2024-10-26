#!/bin/bash

export POSTGRES_ADMIN_PASSWORD_B64=""
export POSTGRES_USER_PASSWORD_B64=""

if [[ -z "$POSTGRES_ADMIN_PASSWORD_B64" || -z "$POSTGRES_USER_PASSWORD_B64" ]]; then
	echo "ERROR: Environment variables not set"
	exit 1
fi

set -x

sed -i "s/<POSTGRES_ADMIN_PASSWORD>/$POSTGRES_ADMIN_PASSWORD_B64/g" secret.yaml
sed -i "s/<POSTGRES_USER_PASSWORD>/$POSTGRES_USER_PASSWORD_B64/g" secret.yaml

cat secret.yaml

helm uninstall postgres --namespace postgres

kubectl delete storageclass postgres
kubectl delete pv postgres

kubectl apply --filename storage.yaml --namespace postgres
kubectl apply --filename secret.yaml --namespace postgres

helm upgrade postgres oci://registry-1.docker.io/bitnamicharts/postgresql --version 1.0.0 --values values.yaml --install --atomic --debug --history-max=3 --namespace postgres

git restore secret.yaml