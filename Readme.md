## Batch Scoring Using Azure Auto ML generated Model

This repo uses the [Telco churn data from Kaggle](https://www.kaggle.com/blastchar/telco-customer-churn) to run a batch scoring script to predict customer churn using classification model generated using Azure AutoML. 
Azure AutoML has been used to create the classification model and is deployed to Azure Container Instance. 
The ACI REST endpoint is used to score the Churn Data and the prediction result is stored in a CSV. 

