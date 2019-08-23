# vin_decode_api

The vin_decode_api expects a VIN, decodes the VIN and provides the make and model year of the vehicle.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc









# vin_decode_api

## Deploy your application to kube cluster:

### Prerequisites:

1. Use existing or create an iam role with with amazonekscluster policy and amazoneksservice policy
2. Use existing or create a cloudformation stack to create vpc  
3. Create EKS-cluster with name "vin_decode_api" along with iam role,vpc and security groups
4. Install kubectl(To communicate with kubernetes) and aws-iam-authenticator(configure aws-iam yaml configured with eks role arn)
5. Use existing or create cloudformation stack to create worker nodes configured with EKS-cluster 
6. To check nodes use "kubectl get nodes"
7. Make sure git and kompose are installed

## Deploy the  application:

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


