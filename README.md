# car_model_with_vin

Deploy your application to kube cluster:
Prerequisites:
1.use existing or create an iam role with with amazonekscluster policy and amazoneksservice policy
2.use existing or create an cloudformation stack to create vpc  
3.Create EKS-cluster with name "car_model_vin" along with iam role,vpc and security groups
3.Install kubectl(To communicate with kubernetes) and aws-iam-authenticator(configure aws-iam yaml configured with eks role arn)
4.Use existing or create cloudformation stack to create worker nodes configured with EKS-cluster 
5.To check nodes use "kubectl get nodes"
6.make sure git and kompose are installed
Deploy an application:
1.git clone https://github.com/srideviraman1407/car_model_with_vin.git car_model_project
2.cd car_model_project
3.Use kompose convert for example from this folder docker-compose.yml to car-model.yaml to car-model-service.yaml gets created
4.Use "kubectl -f car-model.yaml" and "kubectl -f car-model-service.yaml" 
5. make sure service and pods are created by using "kubectl get pods" and "kubectl describe svc car-model"
6. use "kubectl describe svc car-model" to get loadbalancer Ingress or external ip address
for example:http://203.0.113.0:5000/vin/WAUHGAFC6GN017093
Autoscaling based on CPU usage and request:
"kubectl autoscale deployment car-model-vin --cpu-percent=70 --min=1 --max=10"

How continous delivery works:
when develoers push code to github-->jenkins-->create and push docker images to docker registry-->spinnaker pipeline grabs image from docker registry and pushes the image to kubernetes

