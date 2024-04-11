#!/bin/bash
export APP_NAME=supertokens-core
export APP_VERSION=1.0.0

# Need DOCKER_USERNAME and DOCKER_PASSWORD env vars
# Needs secret manifest to be applied
helm registry login 'registry-1.docker.io' --username "$DOCKER_USERNAME" --password "$DOCKER_PASSWORD"
helm package .
helm push ./$APP_NAME-$APP_VERSION.tgz oci://registry-1.docker.io/$DOCKER_USERNAME
helm upgrade $APP_NAME ./$APP_NAME-$APP_VERSION.tgz --install --atomic --debug --history-max=3 -n topfilms