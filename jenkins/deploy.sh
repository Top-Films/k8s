#!/bin/bash

export JENKINS_ADMIN_USERNAME=""
export JENKINS_ADMIN_PASSWORD=""
export JENKINS_CLIENT_ID=""
export JENKINS_CLIENT_SECRET=""
export CA_CERT_PATH=""
export CA_CERT_PRIVATE_KEY_PATH=""

if [[ -z "$JENKINS_ADMIN_USERNAME" || -z "$JENKINS_ADMIN_PASSWORD" || -z "$JENKINS_CLIENT_ID" || -z "$JENKINS_CLIENT_SECRET" || -z "$CA_CERT_PATH" || -z "$CA_CERT_PRIVATE_KEY_PATH" ]]; then
	echo "ERROR: Environment variables not set"
	exit 1
fi

set -x

sed -i "s/<JENKINS_ADMIN_USERNAME>/$JENKINS_ADMIN_USERNAME/g" values.yaml
sed -i "s/<JENKINS_ADMIN_PASSWORD>/$JENKINS_ADMIN_PASSWORD/g" values.yaml
sed -i "s/<JENKINS_CLIENT_ID>/$JENKINS_CLIENT_ID/g" values.yaml
sed -i "s/<JENKINS_CLIENT_SECRET>/$JENKINS_CLIENT_SECRET/g" values.yaml

cat values.yaml

cp $CA_CERT_PATH .
cp $CA_CERT_PRIVATE_KEY_PATH .

kubectl create namespace jenkins

kubectl delete secret jenkins.topfilms.io-tls -n jenkins
kubectl create secret tls jenkins.topfilms.io-tls --cert=cert.pem --key=key.pem -n jenkins

rm cert.pem
rm key.pem

helm uninstall jenkins -n jenkins

kubectl delete pv jenkins

kubectl apply -f storage.yaml -n jenkins
kubectl apply -f sa.yaml -n jenkins

helm repo add jenkinsci https://charts.jenkins.io
helm repo update

helm upgrade jenkins jenkinsci/jenkins -f values.yaml --install --atomic --debug --history-max=3 --namespace jenkins

git restore values.yaml