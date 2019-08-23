# car_model_with_vin

Deploy your application to kube cluster:
Prerequisites:
1.use existing or create an iam role with with amazonekscluster policy and amazoneksservice policy
2.use existing or create an cloudformation stack to create vpc  
3.Create EKS-cluster with name "car_model_vin" along with iam role,vpc and security groups
3.Install kubectl(To communicate with kubernetes) and aws-iam-authenticator(configure aws-iam yaml configured with eks role arn)
4.Use existing or create cloudformation stack to create worker nodes configured with EKS-cluster 
5.To check nodes use "kubectl get nodes"
6.make sure git is installed
Deploy an application:
1.git clone 
