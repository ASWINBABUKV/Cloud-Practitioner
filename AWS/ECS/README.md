
## ECS - ELASTIC CONTAINER SERVICE

-  A fully managed container orchestration service provided by Amazon Web Services (AWS).
- We can deploy, scale, and manage containerized applications.

AWS ECS (Amazon Elastic Container Service) offers two launch types for running containers: EC2 launch type and Fargate launch type.

1. Fargate Launch Type:

- Serverless Compute: With Fargate, you don't need to manage any EC2 instances. AWS automatically provisions and manages the underlying infrastructure required to run your containers.

2. EC2 Launch Type:

- You provision and manage a cluster of EC2 instances to serve as the underlying infrastructure for running your containers.
- You are responsible for managing their scaling, patching, and maintenance.
- This approach offers full control over the underlying infrastructure, allowing you to customize the EC2 instances for specific needs.

Terminologies 

1. Task Definition:

- Blueprint written in json format for how to launch the container
- It defines various parameters required to run containers, such as Docker image, CPU and memory requirements, networking, logging configuration, and other container settings.

2. Task:

- A Task is an instantiation of a Task Definition. It represents a single running instance of the containers defined in the Task Definition.
