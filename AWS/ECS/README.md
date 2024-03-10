# Container Orchestrator

Let's say we are deploying a microservices based application, there will be multiple services. Each service will get its container. Then we need to deploy this somewhere -> (AWS Virtual Machine using EC2 service). We need a container runtime like docker to run the container in the VM. Then we can deploy the container across all servers. 
- What happens when we want to deploy another container? 
- How do we figure out the best server to deploy the container (some containers may have reached their maximum capacity)? 
- Who monitors the server's available resources? 
- What happens if a container crashes? 
- How to scale up your application during the traffic? 

Container Orchestrator handles all of these tasks. So a container orchestrator manages the life cycle of containers. It's going to handle
- Deploying
- Scaling
- Restarting/Destroying containers
- Load-Balancing

Some of the container orchestrators are Kubernetes, Docker Swarm, AWS ECS etc.

# ECS - ELASTIC CONTAINER SERVICE

- AWS-specific container orchestrator

### Working of ECS

- Create a Cluster -> Will contain all of the resources and everything specific to the ECS based application
- ECS will act as the control Plane -> Manage the lifecycle of the container
- ECS is not running for physically running the containers. It is just the brain.
- We need to maintain the infrastructure for running the containers. So we need some servers. So we create EC2 and create servers in it and deploy the containers.
- While using the EC2 we need to manage the instance by our own. We have to do the security updates, install firewalls etc.
- Fargate -> Follows a serverless architecture. When we want to deploy an application, fargate will create services on demand. It configures the memory, the CPU etc. and dynamically create EC2 instances. Fargate will automatically stop the unused EC2 instances, so cost cutting.

# EKS -> ELASTIC KUBERNETES SERVICE

- AWS manages the Control Plane
- Responsible for scaling and all necessary backups
- We need to manage the worker nodes
- Managing and scaling Kubernetes is difficult
- Properly securing Kubernetes increases operational overhead
- EKS integrates with IAM, S3, Security groups etc.
- Self Manage nodes -> You have to do all the work, manage the infrastrutue for the worker nodes. EC2 instances must be managed by users. Install Kubernetes worker processes must be installed like Kubelet, Kube-proxy, Container runtime. You must manage all the updates and security patches.
- Managed node groups -> Automate the provisioning and lifecyle management of EC2 instances.
- Fargate -> AWS manages the nodes. Similar to ECS. 

# ECS VS EKS

- ECS - AWS specific -> vendor lock-in but K8s is open source -> same API across Kubernetes on all cloud provides
- ECS have a simple architecture, Kubernetes is complex but larger community use it
- Pricing for ECS -> no cost for control Plane, only pat for the infrastructure running application (EC2, EBS) and EKS is more expensive.
- When your app isn't too complex and doesnt need to run on K8s prefer ECS. If we are configuring the ECS, its like configuring a docker compose file. We need to provide the list of all containers, configuration for the container and the no. of instances of each container. ECS is cheap.
  
## ECS - ELASTIC CONTAINER SERVICE

-  A fully managed container orchestration service provided by Amazon Web Services (AWS).
- We can deploy, scale, and manage containerized applications.
- Our deployment happens on a cluster. Cluster means groups of EC2 instances.
- Inside an EC2 instance we run a task. It is a way to launch your application. When a task is run then it will run the containers inside it. Task will be run based on the task definition. It is like a blueprint of how the containers should run. It containers the docker image.
- 

AWS ECS (Amazon Elastic Container Service) offers two launch types for running containers: EC2 launch type and Fargate launch type. 

1. Fargate Launch Type:

- Serverless Compute: With Fargate, you don't need to manage any EC2 instances. AWS automatically provisions and manages the underlying infrastructure required to run your containers.

2. EC2 Launch Type:

- You provision and manage a cluster of EC2 instances to serve as the underlying infrastructure for running your containers.
- You are responsible for managing their scaling, patching, and maintenance.
- This approach offers full control over the underlying infrastructure, allowing you to customize the EC2 instances for specific needs.

Terminologies 

1. Task Definition:

- Blueprint written in JSON format for how to launch the container
- It defines various parameters required to run containers, such as Docker image, CPU and memory requirements, networking, logging configuration, and other container settings.

2. Task:

- A Task is an instantiation of a Task Definition. It represents a single running instance of the containers defined in the Task Definition.

3. Service:

- An ECS service allows you to define long-running tasks or services that need to be continuously running. A service ensures that a specified number of tasks are always running and can automatically handle tasks that fail or need to be replaced. It will take care of load balancing and autoscaling. we cannot define these in the task definition. 

4. Load Balancing:

- load balancing is used to distribute traffic across the containers or tasks running within the ECS cluster.
- When you deploy your containers using ECS, you can attach them to a load balancer to distribute incoming traffic across multiple instances of your application. This ensures that the workload is evenly distributed and that the application remains available and responsive even during high-traffic periods. 
