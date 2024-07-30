#!/bin/bash

# kubectl create secret tls auth.topfilms.io-tls --cert=cert.pem --key=key.pem -n keycloak
# kubectl apply -f secret.yaml -n keycloak
echo "$DOCKER_PASSWORD" | helm registry login registry-1.docker.io --username $DOCKER_USERNAME --password-stdin
helm package helm --app-version=23.0.7 --version=23.0.7
helm push ./keycloak-23.0.7.tgz oci://registry-1.docker.io/$DOCKER_USERNAME
helm upgrade keycloak ./keycloak-23.0.7.tgz --install --atomic --debug --history-max=3 -n keycloak --set image.tag=23.0.7