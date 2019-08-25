# vin_decode_api

The vin_decode_api expects a VIN, decodes the VIN and provides the make and model year of the vehicle.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

To Successfully run this API in your localhost, you will need to install

1. git
2. docker

### Installing

Below is the step by step series of examples that tell you how to get the development env running

1. Clone the repository in your local machine using the below command

```
git clone https://github.com/srideviraman1407/vin_decode_api.git
```

2. Change Directory to the folder vin_decode_api

```
cd vin_decode_api
```

3. Build the docker image

```
docker-compose build
```

4. Start containers from the docker image

```
docker-compose up -d
```

5. Verify the container is running 

```
docker ps
```

5. In your browser , call the API using the below example

```
http://localhost:5000/vin/WAUHGAFC6GN017093
```

6. The API will give a response with the make and year of the car based on the VIN provided 

```
{
    "make": "Audi",
    "year": "2016"
}
```

## Running the tests

Case 1: Send a valid VIN  the following WMIs : WAU - Audi , WP0 - Porsche , WVW - Volkswagen
```
http://localhost:5000/vin/WAUHGAFC6GN017093
```
Expected Result :
```
{
    "make": "Audi",
    "year": "2016"
}
```

Case 2: Send a corrupt VIN that is more than 17 characters
```
http://localhost:5000/vin/WAUHGAFC6GN017093jsdhdskdsds
```
Expected result:

```
"car model not found, Please verify your vin and try again"
```

Case 3: Inject the VIN with symbols
```
http://localhost:5000/vin/WAUHGAFC6G%^*17093
```
Expected result:

```
"car model not found, Please verify your vin and try again"
```


## Deployment

#### Prerequisites to deploy the application in a Kubernetes Cluster

1. Use existing or create an iam role with with amazonekscluster policy and amazoneksservice policy
2. Use existing or create a cloudformation stack to create vpc  
3. Create EKS-cluster with name "vin_decode_api" along with iam role,vpc and security groups
4. Install kubectl(To communicate with kubernetes) and aws-iam-authenticator(configure aws-iam yaml configured with eks role arn)
5. Use existing or create cloudformation stack to create worker nodes configured with EKS-cluster 
6. To check nodes use "kubectl get nodes"
7. Make sure git and kompose are installed if docker-compose.yaml file is used

#### Deploy the application in a Kubernetes Cluster

1. git clone https://github.com/srideviraman1407/vin_decode_api.git
2. Use kompose convert for example from this folder docker-compose.yml to vin_decode.yaml to vin_decode_service.yaml gets created
3. Use 'kompose convert' and 'kubectl create -f'  
4. Make sure service and pods are created by using "kubectl get pods" and "kubectl describe svc car-model"
5. Use "kubectl describe svc car-model" to get loadbalancer Ingress or external ip address
for example:http://203.0.113.0:5000/vin/WAUHGAFC6GN017093
Autoscaling based on CPU usage and request:
"kubectl autoscale deployment car-model-vin --cpu-percent=70 --min=1 --max=10"

## Auto Scaling :

Auto-scaling the number of instances of the API based on:

1. CPU usage

Autoscaling is natively supported in Kubernetes. By default, you can automatically scale the number of Kubernetes pods based on the observed CPU utilization. 
```
    "kubectl autoscale deployment vin_decode_api_web --cpu-percent=70 --min=1 --max=10"
```
2. Number of requests

To scale your application based on other monitored metrics, such as the number of incoming requests or the memory consumption, we can achieve that by leveraging the Prometheus and Kubernetes aggregator layers.

Prometheus is widely used to monitor all the components of a Kubernetes cluster including the control plane, the worker nodes, and the applications running on the cluster.

We can deploy the application and a HPA rule to autoscale with http_requests metric collected and exposed via Prometheus. The HPA rule allows us to scale the application pods between 2 and 10 replicas, and all pods serve a total of 100 requests per second.

1. Configure the Kubernetes cluster to enable the aggregator layer and autoscaling API group.
2. Deploy a Prometheus monitoring system.
3. Deploy a custom API server and register it to the aggregator layer.
4. Deploy a sample application and test the autoscaling.

The custom API server we will use here is a Prometheus adapter which can collect metrics from Prometheus and send them to the HPA controller via REST queries 

Here is a sample metrics app that can be used to autoscale based on number of requests (http_request)

```
cat sample-metrics-app.yaml
...
---
kind: HorizontalPodAutoscaler
apiVersion: autoscaling/v2alpha1
metadata:
name: sample-metrics-app-hpa
spec:
    scaleTargetRef:
        kind: Deployment
        name: sample-metrics-app
    minReplicas: 2
    maxReplicas: 10
    metrics:
    - type: Object
    object:
        target:
        kind: Service
        name: sample-metrics-app
        metricName: http_request
        targetValue: 100
 ```
 
 Apply the recently created HPA rule as shown below:
 
  ```
 kubectl create -f sample-metrics-app.yaml

deployment "sample-metrics-app" created
service "sample-metrics-app" created
servicemonitor "sample-metrics-app" created
horizontalpodautoscaler "sample-metrics-app-hpa" created
kubectl get hpa

NAME                     REFERENCE                       TARGETS      MINPODS   MAXPODS   REPLICAS   AGE
sample-metrics-app-hpa   Deployment/sample-metrics-app   866m / 100   2         10        2          1h

 ```
The HPA controller will scale up the number of application pods, based on the loads hitting the sample application service.

## Continuous Delivery :

We will use a continuous delivery platform like Spinnaker for releasing software changes rapidly and reliably. Spinnaker makes it easier for developers to focus on writing code without having to worry about the underlying cloud infrastructure. It integrates seamlessly with Jenkins and other popular build tools.

The below diagram showcases how to build a continuous delivery pipeline for workloads running on Kubernetes. 

![alt text](https://github.com/srideviraman1407/vin_decode_api/blob/master/CI:CD_Pipeline.png)

These steps are covered in the diagram:

* Developer pushes code to GitHub.
* GitHub triggers Jenkins.
* Jenkins builds a Docker image, tags and pushes it to repostitory management service like JFrog Artifactory.
* The Spinnaker pipeline is triggered when JFrog Artifactory receives the new Docker image.
* Spinnaker then does following:
    * Generate (bake) Kubernetes deployment files (dev and prod) using Helm.
    * Deploy Kubernetes to the dev environment.
    * Manual judgement: The pipeline configuration requires a manual confirmation by a human before it can deploy the app to production. It will wait at this step before pipeline execution can continue.
    * Deploy the code to the production environment.

## Authentication :

While building an API based architecture, it is common practice to build a common security layer around these APIs, basically on the edge so that all the APIs are secured. There are multiple ways to build API security like writing some filters in the case of Java / J2EE application, installing some agents in front of APIs which can make policy decisions etc. One of the most widely used protocol for Authorization is OAuth2. 

We can use the OAuth 2.0 Client Credentials Flow. This is a way of letting two servers communicate with each other, without the context of a user. The two servers must agree ahead of time to use a third-party authorization server. Assume there are two servers, A and B, and an authorization server. Server A is hosting the REST API, and Server B would like to access the API.

Server B sends a secret key to the authorization server to prove who they are and asks for a temporary token.
Server B then consumes the REST API as usual but sends the token along with the request.
Server A asks the authorization server for some metadata that can be used to verify tokens.
Server A verifies the Server B’s request.
If it’s valid, a successful response is sent and Server B is happy.
If the token is invalid, an error message is sent instead, and no sensitive information is leaked.

Best practices for such an architecture involves using some kind of API platform / Gateway like Apigee, Kong or AWS API Gateway approach to Design, secure, analyze and monitor all the APIs.



## Authors

* **Sridevi Raman** - *Initial work* - [srideviraman1407](https://github.com/srideviraman1407)


