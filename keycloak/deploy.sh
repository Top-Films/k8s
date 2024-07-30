#!/bin/bash

# kubectl create secret tls auth.topfilms.io-tls --cert=cert.pem --key=key.pem -n keycloak
# kubectl apply -f secret.yaml -n keycloak
echo "$DOCKER_PASSWORD" | helm registry login registry-1.docker.io --username $DOCKER_USERNAME --password-stdin

      - run:
          name: Helm package
          command: helm package helm/$APP_NAME --app-version=$APP_VERSION --version=$APP_VERSION

      - run:
          name: Helm artifact push
          command: helm push ./$APP_NAME-$APP_VERSION.tgz oci://registry-1.docker.io/$DOCKER_USERNAME

      - run:
          name: Helm deploy
          command: helm upgrade $APP_NAME ./$APP_NAME-$APP_VERSION.tgz --install --atomic --debug --history-max=3 -n topfilms --set image.tag=$APP_VERSION