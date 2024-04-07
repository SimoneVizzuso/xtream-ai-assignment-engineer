# Challenge 4

I opted to use Amazon as my provider, specifically the SageMaker service.

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

It is important to set up versioning of the models and run experiments so you can understand how they have been changed over time, if there is a problem with a latest model being able to easily go back to the previous one or keep track of improvements

It is feasible to use the Experiments SDK to run experiments on the models. By tracking with logs the metrics and results of the models it is possible to have a history to reproduce the results and help in a potential debugging case

Versioning is done through the possibility of labeling, thanks to the Model Registry, the various runs of the trainings in order to have a record of them for the reasons proposed above.

A tag and categorization of the model can be established to easily recognize it and deploy it quickly. Again, various parameters and permissions can be modified to automate or require human review before a model goes into production.

## Deploy the model in production

After verifying that the model is trained and that the preprocessing jobs are configured properly, we can use the pre-built containers of the service to build the code that will act as an intermediary with the model, defining how to provide it with inputs and handling the outputs generated, then to allow us to make inferences about the model.

Set the type of instance on which to deploy the model based on the expected traffic volume, desired latency, and other factors. One can also set up Autoscaling so as to automate scaling so as to handle any spikes in traffic.

After that it is possible to configure the endpoint from which to call the model so that it will be available an URL to call in order to do inference. All that is left to do at this point is to test, monitor the responses, and possibly, with versioning, keep the model up to date.
