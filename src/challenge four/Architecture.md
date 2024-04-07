# Challenge 4

I opted to use Amazon as my provider, specifically the SageMaker service. Every time I'll refer to "the service" I'll be referring to SageMaker.

## Configure the data storage

First we need to store the dataset in a secure and customized location: let’s create a bucket in the Amazon S3 service, configuring the different parameters like versioning, encryption, and access control.

Then we can upload our dataset in the bucket and start to organize the data for receiving new data in the future (we are developing a continuous learning environment from the second challenge).

After configuring the different users and grants the different access permissions to the bucket, setting up the logging and enabling versioning to have the history of the future changes, we are ready to start with the processing of the data.

## Automate preprocessing of the data

Having worked on preprocessing automation during the previous challenges, we need to define precisely what the lacking points are and optimize the preprocessing script so that it is compatible with SageMaker Processing containers.

In this case we need to create a job called SageMaker Processing, configuring it to take the data where we loaded it, save the result, and give it further details about the types of data it will process.

One will then be able to monitor the job through its console. At the end of the computation we will have the processed data. We then just need to automate everything by setting up, with AWS tools, a periodic schedule so that as it receives the data it can preprocess it automatically.

## Build the training infrastructure

Again, in this case we already have our model which, after any improvements, and after checking its compatibility with the service, can be used.

Once we have created the base with which to load the data and preprocess it, we go on to create another job, this time for our model. It will be necessary to evaluate, with our model template, the parameters to be provided to the job for optimal configuration.

After testing that the job works, that the model is trained, that evaluations are given, we can deploy the model to an endpoint provided by SageMaker, and it will be possible to call it and use its prediction functions

## Setup the model versioning and logging

It is important to set up versioning of the models and run experiments so you can understand how they have been changed over time, if there is a problem with a latest model being able to easily go back to the previous one or keep track of improvements.

It is feasible to use the Experiments SDK to run experiments on the models. By tracking with logs the metrics and results of the models it is possible to have a history to reproduce the results and help in a potential debugging case.

Versioning is done through the possibility of labeling, thanks to the Model Registry, the various runs of the trainings in order to have a record of them for the reasons proposed above.

A tag and categorization of the model can be established to easily recognize it and deploy it quickly. Again, various parameters and permissions can be modified to automate or require human review before a model goes into production.

## Deploy the model in production

After verifying that the model is trained and that the preprocessing jobs are configured properly, we can use the pre-built containers of the service to build the code that will act as an intermediary with the model, defining how to provide it with inputs and handling the outputs generated, then to allow us to make inferences about the model.

Set the type of instance on which to deploy the model based on the expected traffic volume, desired latency, and other factors. One can also set up Autoscaling so as to automate scaling so as to handle any spikes in traffic.

After that it is possible to configure the endpoint from which to call the model so that it will be available an URL to call in order to do inference. All that is left to do at this point is to test, monitor the responses, and possibly, with versioning, keep the model up to date.

## Manage the API Gateway
With Amazon API Gateway it is possible to create REST APIs to access, just set up the API endpoints to interact with those in the model and it will be possible to implement GET, POST, etc.

It will then be necessary to configure the API Gateway to result as a backend service in a SageMaker endpoint. it is then necessary to set up the request and response mapping and ensure that they accurately manage input validation, data transformation, and error handling.

Again it is possible to deploy the API so that it can be accessed by the client. Next it is important to take care of the security part with the IAM provided by AWS or other authentication systems.

## Handle the load balance
It is also important to manage the load to distribute requests to the API at multiple instances. This is achieved by creating a Load Balancer through the EC2 service. It is possible to create both an Application Load Balancer (ALB) and a Network Load Balancer (NLB).

You then define target groups that will receive traffic from the LB by specifying various configuration parameters. A health monitor will also be provided to see if a target is available to receive traffic. This will also allow constant monitoring of the status in which the targets are working

Connecting it all to the service, finishing fixing the configuration and security parameters will be enough to test and these services will be available to distribute the calls so that the system can be easily scaled up and made always available even if some of the targets fail

## Logging and monitoring with alarms

To monitor the infrastructure and make sure that one is constantly updated on possible problems that will, most certainly, happen, it is necessary to set up a service called CloudWatch. It will be possible to set up metrics to monitor such as invocation counts, latency, and error rates and make sure that you are notified if there are any problems.

In this case you can set up the so-called alarms that will be sent based on the parameters provided such as a threshold not to be exceeded or even just a period after which to send a message anyway.

For this to work there is a need to set up that the endpoints send logs directly to CloudWatch for real-time analysis. From here all logging policies can be set, from the time for which to keep them to how to archive them.

## Thinking about security

It is also critical to take care of security: as mentioned earlier, it is important to carefully set up the Identity and Access Management (IAM) provided by AWS for different parts of the infrastructure. This can be done by creating different roles and giving them different permissions based on the intended policy.

Again with the AWS tools, it is possible to set up an encription of the data in the buckets or internal and client connections. If all the infrastructure and data have been built within AWS it will certainly be easier to manage the security of the same since many services work in sync with the endpoints, user roles, network and data.

## Other possible consideration

There are numerous issues to keep in mind when finalizing an architecture, for example, cost optimization, automatic resource scaling, backup management, and GRC (Governance Risk Compliance):
- For cost optimization, cost allocation tags can be used to track them and observe how they could be worked on to reduce or contain them. However, this must be coupled with careful analysis and application of optimization strategies
- On the automatic scaling of resources, extreme care must be taken because cloud services are notorious for, if not configured properly, scaling excessively and later presenting an exorbitantly expensive bill.
Depending on utilization, one can set values (such as CPU utilization, wait times, and queued users) so that resources can be scaled up, but as mentioned before one must be careful that these resources do not only scale up for a period, and thus there is no need to scale up the entire architecture but only to amplify the service for a short period.
- Backup, and therefore all disaster recovery play a key role in any data-populated environment. It is important to set up a regular backup system to avoid data loss. Equally important is to test backups from time to time to make sure they are still intact and functioning.
- Last but not least, the whole topic related to data and security legislative regulations including GDPR, HIPAA, and PCI DSS. Necessary, penalty related implications, to adhere to regulations and implement security and control systems that are compliant with the requirements of the governments where the service is deployed or provided.