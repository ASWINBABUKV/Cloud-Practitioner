

# AWS EKS

Creating an AWS Elastic Kubernetes Cluster and deploying a simple application on it


## Steps to Create EKS Cluster


![Screenshot 2024-02-23 004955](https://github.com/ASWINBABUKV/Cloud-Practitioner/assets/137376192/f1a666ea-63f7-4c4b-8966-def9ea1fd78e)

1. Create a VPC for the EKS Cluster using the Cloud Formation Template

    _VPC stands for virtual private cloud._ Create a separate VPC for the EKS Cluster. We can use a cloud formation template for creating the VPC. CloudFormation template provides a standardized and automated way to create a VPC suitable for hosting Amazon EKS clusters


- Go to AWS Cloud Formation Service
- Create a stack
- Template is ready (since we are using a pre-defined template)
- Specify the S3 URL
```bash
  https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml
```
- Enter Stack Name -> EKSVPCCloudFormation
- Create Stack

  Why VPC?

VPC provides a secure and isolated environment for running your EKS cluster, ensuring that your Kubernetes resources are protected and can communicate securely within the cloud. It gives you control over the networking configuration and allows integration with other AWS services, enhancing the flexibility and security of your containerized applications.

  In the context of Amazon EKS, a VPC is required to provide networking infrastructure for the Kubernetes cluster. It enables communication between EKS control plane components, worker nodes, and other AWS services. The VPC also allows you to configure networking policies, such as pod-to-pod communication.

  The provided CloudFormation template (amazon-eks-vpc-private-subnets.yaml) is a YAML file that defines the resources needed to create a VPC suitable for hosting an Amazon EKS cluster. This template sets up a VPC with private subnets across multiple Availability Zones.

  Parameter section -> It's like how big your VPC should be.

  VpcBlock -> The CIDR range for the VPC, which defines the IP address range for the VPC.

  Resources Section -> This section lists all the things we're going to create in our virtual network.
  - InternetGateway: An internet gateway attached to the VPC to enable outbound internet access for resources within the VPC.
  - VPCGatewayAttachment: Attachment of the internet gateway to the VPC.
  - PublicRouteTable: Route table for public subnets.
  - PrivateRouteTable01, PrivateRouteTable02: Route tables for private subnets in different Availability Zones.
  - NatGateway01, NatGateway02: NAT gateways for private subnets in each Availability Zone to enable internet access for resources in private subnets.
  - PublicSubnet01, PublicSubnet02: Public subnets in different Availability Zones.
  - PrivateSubnet01, PrivateSubnet02: Private subnets in different Availability Zones.

  Outputs Section -> This section defines the outputs of the CloudFormation stack
  - SubnetIds: IDs of all subnets created within the VPC.
  - SecurityGroups: Security group for controlling communication between the EKS control plane and worker nodes.
  - VpcId: ID of the VPC created by the stack.

  Explanation of what this does?

  - The template creates a VPC with specified CIDR blocks and divides it into public and private subnets across multiple Availability Zones.
  - Public subnets have internet access through an internet gateway, while private subnets use NAT gateways for outbound internet access.
  - Route tables are configured to route traffic appropriately between the subnets and the internet.
  - Security groups are defined to control inbound and outbound traffic between resources within the VPC.
  - The outputs provide information such as subnet IDs and VPC IDs for use in other CloudFormation templates or scripts.

2. Create an IAM (Identity and Access Management) Role to create an EKS Cluster

The IAM role is needed to tell Amazon EKS who is allowed to do what within the system. It is like a set of rules that ensure only the right people (or services) have access to the right parts of Amazon EKS, keeping everything safe and organized.

- Go to IAM Service
- Click "Roles" in the left-hand navigation pane
- Create Role 
- Entity Type -> AWS service
- Choose the Use Case -> EKS -> EKS Cluster
- Attach policies -> Search for and attach the below policy. This policy provides necessary permissions for managing EKS resources such as creating and managing clusters.
```bash
  AmazonEKSClusterPolicy
```
- Role Name -> EKSCLusterRole
- Create Role

3. Create EKS Cluster (Control Plane)
- Go to EKS Service
- Create a Cluster with the name EKS-Cluster
- Give the role as EKSCLusterRole (Select the IAM role that we created earlier for the EKS cluster's control plane)
- Allow Cluster Administrator Access -> They can perform any action on the cluster, including creating, modifying, and deleting resources
- Secrets Encryption: Protects sensitive information (secrets) stored in Kubernetes, such as API tokens or passwords. Once you activate secrets encryption, you can't change your mind later. It's a permanent decision. First, the secret itself is encrypted using a unique key. Then, this key is encrypted using a master key managed by AWS KMS (Key Management System). [Leave it as default for demo]
- Tag-> A tag in AWS is like putting a label on your belongings. Tags help to organize and manage resources in AWS. [leave it default]
- Use the custom VPC (select the VPC created earlier)
- Security group related to VPC should be selected
- Cluster endpoint access -> Public and Private
- Create the cluster

4. Create Ubuntu EC2 Instance to access the Cluster
- Go to EC2 Service
- Launch Instance -> K8s-ClientVM
- Select the OS - Ubuntu
- Key-pair - generate new / use existing
- Security group -> Generate new
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

- Install kubectl (Client Machine should perform operations with control Plane)
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
- Download and configure the AWS Command Line Interface (CLI)
```bash
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  sudo ./aws/install
```
- Configure AWS CLI with credentials
```bash
  aws configure
```
_Go to the security credential of the root account. Create the access key._
- List the Cluster
```bash
  aws eks list-clusters
```

6. Configure the Cluster data (Connect the Control Plane and EC2 Instance)
```bash
  aws eks update-kubeconfig --name <cluster-name> --region <region-code>
```
- In the cluster, we will have kubeconfig file which contains cluster information. Update the kubeconfig file to connect kubectl and Control Plane.
- Use 'cat' Command to see the content inside kubeconfig file
- Next, add Worker Nodes to the Control Plane. For that 

7. Create an IAM Role for the EKS Worker Nodes with the below policies
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

## Successfully Created Control Plane and Worker Nodes (Kubernetes CLuster)

### Deploying the Application


1. Download the files

    _This is a basic HTML form that takes the input from the user and will store the input in a text file. We can display, search, and delete users._

2. Install docker
   
```bash
sudo apt update
sudo apt install docker.io -y
sudo snap install docker
```
check whether docker is installed 
```bash
docker --version
OR
sudo systemctl status docker
```
4. Build the docker image

- docker build -t <image_name> .

```bash
docker build -t text-app .
```
3. Push the image to the docker hub

- docker tag <image_name> <dockerhub_user_id>/<image_name>
- docker push <dockerhub_user_id>/<image_name>

```bash
docker tag text-app aswin1101/text-app
docker push aswin1101/text-app
```
4. Check whether the container is running

```bash
docker ps
```

5. Run the docker container

```bash
docker run -d my-image
docker run -d -p 8080:80 my-image

#-d: Detached mode, which means the container runs in the background.
#-p 8080:80: Maps port 8080 on the host to port 80 in the container. This allows accessing the containerized application via port 8080 on the host machine.

```
6. Build the deployment and service files (textapp.yaml)
```bash
kubectl apply -f textapp.yaml
```

7. Check the status of your deployment and service to ensure that your application is running correctly.
```bash
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get pods -o wide
```

8. Copy and paste the DNS of the load balancer



![Screenshot 2024-02-23 151156](https://github.com/ASWINBABUKV/Cloud-Practitioner/assets/137376192/f06de7cb-cd5d-426b-96f4-67819d86f53f)
