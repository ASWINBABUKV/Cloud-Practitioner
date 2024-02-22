

# AWS EKS

Creating an AWS Elastic Kubernetes Cluster and deploying a simple application on it


## Steps to Create EKS Cluster


![Screenshot 2024-02-23 004955](https://github.com/ASWINBABUKV/Cloud-Practitioner/assets/137376192/f1a666ea-63f7-4c4b-8966-def9ea1fd78e)

1. Create a VPC for the EKS Cluster using Cloud Formation Template
- Go to AWS Cloud Formation Service
- Create a stack
- Template is ready
- Give the S3 URL
```bash
  https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml
```
- Enter Stack Name -> EKSVCCloudFormation
- Create a new key-value pair
- Create Stack
_VPC stands for virtual private cloud._

2. Create IAM (Identity and Access Management) Role in AWS
- Go to IAM Service
- Create Role 
- Entity Type -> AWS service
- Usecase -> EKS -> EKS Cluster
```bash
  AmazonEKSClusterPolicy
```
- Role Name -> EKSCLusterRole
- Create Role

3. By using the VPC and Role, create EKS Cluster (Control Plane)
- Go to EKS Service
- Create Cluster with name EKS-Cluster
- Give the role as EKSCLusterRole
- Use the custom VPC
- Security group related to VPC should be selected
- Cluster endpoint access -> Public and Private
- Create the cluster

4. Create Ubuntu EC2 Instance to access the Cluster
- Go to EC2 Service
- Launch Instance -> K8s-ClientVM
- Key-pair - generate new / use old
- Security group -> existing 
- Launch Instance

5. Connect EC2 Instance using terminal (Linux)
- Go to the downloads folder (location of the pem file)
```bash
  ssh -i <pemfile_name> ubuntu@<public_ip_address>
```
- Error will occur -> Permissions for pemfile are too open.
- Change the Permissions
```bash
  chmod 600 <pemfile_name>
```
- Try commands
```bash
  whoami
  apt update
```
- Switch to the root user
```bash
  sudo su -
```
- Install kubectl (Client Machine should perform operations with client Machine)
```bash
     curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```
```bash
     sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```
- Test to ensure the version you installed is up-to-date
```bash
     kubectl version --client
```
- Download and configure AWS Command Line Interface (CLI)
```bash
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  sudo ./aws/install
```
- Configure AWS CLI with credentials
```bash
  aws configure
```
_Go to security credential of root account. Create the access key._
- List the Cluster
```bash
  aws eks list-clusters
```

6. Configure the Cluster data (Connect the Control Plane and EC2 Instance)
```bash
  aws eks update-config --name <cluster-name> --region <region-code>
```
- In the cluster we will have kubeconfig file which contains cluster information. Update the kubeconfig file to connect kubectl and Control Plane.
- Use <cat> Command to see the content inside kubeconfig file
- Next, add Worker Nodes to the Control Plane. For that 

7. Create IAM Role for the EKS Worker Nodes with below policies
```bash
  AmazonEKSWorkerNodePolicy
  AmazonEKS_CNI_Policy
  AmazonEC2ContainerRegistryReadOnly
```
- Go to IAM Service -> Create Role named EKSWorkerNodeRole
- Use case - EC2
- Select the above 3 policies

8. Create Worker Node Group in the Cluster
- Go to the Cluster -> Compute option -> Add node group (EKS-Node-Group)
- Role -> EKSWorkerNodeRole

Try commands
```bash
  kubectl get nodes   
  kubectl get pods
```

## Sucessfully Created Control Plane and Worker Nodes

