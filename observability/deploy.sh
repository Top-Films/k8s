# helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
# helm repo update
# helm pull prometheus-community/prometheus --untar
# helm install prometheus prometheus-community/prometheus --namespace observability

helm repo add grafana https://grafana.github.io/helm-charts 
helm repo update
# helm pull grafana/grafana --untar
helm upgrade grafana grafana/grafana --values values.yaml --install --atomic --debug --history-max=3 --namespace observability