export GRAFANA_CLIENT_ID=""
export GRAFANA_CLIENT_SECRET=""
export CA_CERT_PATH=""
export CA_CERT_PRIVATE_KEY_PATH=""

if [[ -z "$GRAFANA_CLIENT_ID" || -z "$GRAFANA_CLIENT_SECRET" || -z "$CA_CERT_PATH" || -z "$CA_CERT_PRIVATE_KEY_PATH" ]]; then
	echo "ERROR: Environment variables not set"
	exit 1
fi

sed -i "s/<GRAFANA_CLIENT_ID>/$GRAFANA_CLIENT_ID/g" grafana-values.yaml
sed -i "s/<GRAFANA_CLIENT_SECRET>/$GRAFANA_CLIENT_SECRET/g" grafana-values.yaml

cp $CA_CERT_PATH .
cp $CA_CERT_PRIVATE_KEY_PATH .

kubectl delete secret grafana.topfilms.io-tls --namespace observability
kubectl create secret tls grafana.topfilms.io-tls --cert=cert.pem --key=key.pem --namespace observability

rm cert.pem
rm key.pem

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade prometheus prometheus-community/prometheus --values prometheus-values.yaml --install --atomic --debug --history-max=3 --namespace observability

helm repo add grafana https://grafana.github.io/helm-charts 
helm repo update
helm upgrade grafana grafana/grafana --values grafana-values.yaml --install --atomic --debug --history-max=3 --namespace observability
helm upgrade loki grafana/loki --values values.yaml --install --atomic --debug --history-max=3 --namespace observability

git restore grafana-values.yaml