#!/bin/bash

# Must have:
# - Select a node and add the label postgres-port-forwarded: 'true'
# - The node with the postgres-port-forwarded: 'true' must have 30543 port forwarded
# - Apply the pv manifest
helm install db oci://registry-1.docker.io/bitnamicharts/postgresql --namespace topfilms -f values-with-secrets.yaml