<p align="center">
  <img src="https://raw.githubusercontent.com/Top-Films/assets/main/png/top-films-logo-white-transparent.png" width="400" alt="logo"/>
  <br><br>
</p>

![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
![Postgres](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=Jenkins&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

## Overview
This repository holds all of Top Films' Kubernetes files, including manifests, helm charts, and Jenkins files for deployment. Instructions can be found below for specific items.

## Prerequisites
- A MicroK8s Cluster
- Kubectl
- Helm

💡 Note that the commands used in the instructions contains aliases. You can use the following to add the alias's to your bash profile. If you are using Windows and Git Bash, disregard sudo.

```bash
# Add the following to your VMs or machines running MicroK8s
echo "alias k=\"sudo microk8s kubectl\"" >> .bashrc
echo "alias kubectl=\"sudo microk8s kubectl\"" >> .bashrc
echo "alias m=\"sudo microk8s\"" >> .bashrc
bash
```

## Creating a MicroK8s Cluster Ubuntu
1. Download install and run MicroK8s.

```bash
sudo snap install microk8s --classic
```

2. Enable ingress, kubernetes dashboard, and cert manager

```bash
m enable ingress
m enable dashboard
m enable cert-manager
```

3. Expose the Kube API to external networks to connect from a different machine

💡 Note that this is not the most secure way to get access to a cluster from a local machine. If possible, VPN into the network running K8s.

```bash
# Navigate to the MicroK8s certs file
sudo nano /var/snap/microk8s/current/certs/csr.conf.template

# Add your external IP and DNS domain (if you have one) to the alt names
# i.e. DNS.6 = kube-api.domain.com and IP.3 = xx.xx.xx.xx

# Refresh certificates
sudo microk8s refresh-certs --cert server.crt

# Display the config that you will copy to your local kube config
m config

# Change the value of server to either the external ip or domain with the port 16443
# i.e. server: https://kube-api.domain.com:16443

# Verify it works with the following
k version
```

4. Add a worker node(s)

```bash
# Run the following on the master node
m add-node

# Copy the command given and run it in a worker node that has MicroK8s installed
m join ...
```

## Contributing
Contributions are welcome! If you'd like to contribute to the project, please follow these steps:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes and commit them.
- Push your changes to your fork.
- Submit a pull request to the main repository.

## License
This project is licensed under the Apache 2.0 License with Commons Clause.