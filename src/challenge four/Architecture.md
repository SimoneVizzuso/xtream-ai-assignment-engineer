# Challenge 4
I opted to use Amazon as my provider, specifically the SageMaker service.
## Configure the data storage
First we need to store the dataset in a secure and customized location: let’s create a bucket in the Amazon S3 service, configuring the different parameters like versioning, encryption, and access control.

Then we can upload our dataset in the bucket and start to organize the data for receiving new data in the future (we are developing a continuous learning environment from the second challenge).

After configuring the different users and grants the different access permissions to the bucket, setting up the logging and enabling versioning to have the history of the future changes, we are ready to start with the processing of the data.
## Automate preprocessing of the data
