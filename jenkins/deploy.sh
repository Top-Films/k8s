#!/bin/bash

export JENKINS_ADMIN_USERNAME=""
export JENKINS_ADMIN_PASSWORD=""
export JENKINS_CLIENT_ID=""
export JENKINS_CLIENT_SECRET=""
export CA_CERT_PATH=""
export CA_CERT_PRIVATE_KEY_PATH=""

sed -i "s/<JENKINS_ADMIN_USERNAME>/$JENKINS_ADMIN_USERNAME/g" values.yaml
sed -i "s/<JENKINS_ADMIN_PASSWORD>/$JENKINS_ADMIN_PASSWORD/g" values.yaml
sed -i "s/<JENKINS_CLIENT_ID>/$JENKINS_CLIENT_ID/g" values.yaml
sed -i "s/<JENKINS_CLIENT_SECRET>/$JENKINS_CLIENT_SECRET/g" values.yaml

cp $CA_CERT_PATH .
cp $CA_CERT_PRIVATE_KEY_PATH .

kubectl delete secret jenkins.topfilms.io-tls -n jenkins
kubectl create secret tls jenkins.topfilms.io-tls --cert=cert.pem --key=key.pem -n jenkins

rm cert.pem
rm key.pem

kubectl delete pv jenkins -n jenkins

kubectl apply -f storage.yaml -n jenkins
kubectl apply -f sa.yaml -n jenkins

helm uninstall jenkins -n jenkins

helm repo add jenkinsci https://charts.jenkins.io
helm repo update

helm upgrade jenkins jenkinsci/jenkins -f values.yaml --install --atomic --debug --history-max=3 --namespace jenkins

git restore values.yaml