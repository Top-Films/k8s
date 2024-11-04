#!/bin/bash

curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install-edge | sh
export PATH=$HOME/.linkerd2/bin:$PATH
linkerd version
linkerd check --pre
linkerd install --crds | kubectl apply -f -
linkerd install | kubectl apply -f -
linkerd check

# SMI
curl -sL https://linkerd.github.io/linkerd-smi/install | sh
linkerd-smi install | kubectl apply -f - # docs say "linkerd smi ..." but needs -
linkerd-smi check
helm repo add l5d-smi https://linkerd.github.io/linkerd-smi
helm install linkerd-smi -n linkerd-smi --create-namespace l5d-smi/linkerd-smi
