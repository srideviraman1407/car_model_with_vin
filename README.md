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

case 1: send the character more than 17 
http://localhost:5000/vin/WAUHGAFC6GN017093jsdhdskdsds
expected result:
"car model not found, Please verify your vin and try again"

case 2: inject the string with symbols
http://localhost:5000/vin/WAUHGAFC6G%^*17093
expected result:
"car model not found, Please verify your vin and try again"



## Deployment

#### Prerequisites to deploy the application in a Kubernetes Cluster

1. Use existing or create an iam role with with amazonekscluster policy and amazoneksservice policy
2. Use existing or create a cloudformation stack to create vpc  
3. Create EKS-cluster with name "vin_decode_api" along with iam role,vpc and security groups
4. Install kubectl(To communicate with kubernetes) and aws-iam-authenticator(configure aws-iam yaml configured with eks role arn)
5. Use existing or create cloudformation stack to create worker nodes configured with EKS-cluster 
6. To check nodes use "kubectl get nodes"
7. Make sure git and kompose are installed

#### Deploy the application in a Kubernetes Cluster

1. git clone https://github.com/srideviraman1407/vin_decode_api.git
2. Use kompose convert for example from this folder docker-compose.yml to vin_decode.yaml to vin_decode_service.yaml gets created
3. Use "kubectl -f car-model.yaml" and "kubectl -f car-model-service.yaml" 
4. Make sure service and pods are created by using "kubectl get pods" and "kubectl describe svc car-model"
5. Use "kubectl describe svc car-model" to get loadbalancer Ingress or external ip address
for example:http://203.0.113.0:5000/vin/WAUHGAFC6GN017093
Autoscaling based on CPU usage and request:
"kubectl autoscale deployment car-model-vin --cpu-percent=70 --min=1 --max=10"

## Continuous Delivery :

when developers push code to github-->jenkins-->create and push docker images to docker registry-->spinnaker pipeline grabs image from docker registry and pushes the image to kubernetes

![alt text](https://github.com/srideviraman1407/vin_decode_api/blob/master/CI:CD_Pipeline.png)

## Authentication :

Secure the api that require an api Key:
Following are things to be done :
--> Create an API proxy that requires an API key/
--> Add a developer and register an app
--> Call your API with an API key.
Steps to  follow:
Create an API proxy that requires an API key
1. https://apigee.com/edge sign in with the user credentials
2. create API Proxies --> Add proxy--> select reverse proxy-->Enter existing API,proxy name,base path and description
3. Build and deploy
verify the policy
click on api key --> develop tab-->check the api key has been generated
Add image
Try to call api key in browser:
For example :
http://api.example.com
return Hello, Guest!
Create a devoloper and register an app
select publish developer , add developer enter details and click create
register an app:

    Select Publish > Apps.
    Click + App.
    Enter the following in the New Developer App window:
    In this field 	do this
    Name and Display Name 	Enter: keyser_app
    Developer 	Select: Keyser Soze (keyser@example.com)
    Callback URL and Notes 	Leave blank
    In the Credentials section, click to specify the Credentials.
    In the Add credential popup, select Never, and then select OK. The credentials for this app will never expire.
    Under Products, click Add product.
    Select helloworld_apikey-Product.
    Click Add.
Get the API key

To get the API key:

    On the Apps page (Publish > Apps), click keyser_app.
    On the keyser_app page, click Show in the Consumer Key column. Notice that the key is associated with the "helloworld_apikey Product". Click Hide to hide the key.
    Select and copy the Consumer Key. You'll use it in the next step.
Call API with a key:
http://{silvercar}-test.apigee.net/helloapikey?apikey=apikey

## Authors

* **Sridevi Raman** - *Initial work* - [srideviraman1407](https://github.com/srideviraman1407)


