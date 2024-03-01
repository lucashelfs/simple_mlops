# MLE Simple Project with Databricks CE

The ETL, EDA and model training was done in a Databricks Community edition environment, which does not
offer the full features that Databricks can provide, such as the CLI. From the start, I just sent the Test.csv and Train.csv to Databricks using the UI, and then I executed the notebooks on their environment.

The notebooks that I developed on their env are in the folder *Databricks Notebooks*. After training the model there, I downloaded the artifacts from the vanilla run that was executed and have stored the model related files on the folder *mlflow_model* and the other artifacts on the folder *mlflow_artifacts*.

# Predictions app

## Installing Anaconda
You can install Anaconda from their (website)[https://www.anaconda.com/download].

After the installing, you can check if the installation was done properly with the command `conda --version`

## Creating a conda environment with the neccessary dependencies

To create the right environment for running the predictions app, run the following command, which uses Anaconda:

`conda env create --file mlflow_model/conda.yaml --name ml_env`

After creating the environment, activate it with the following command:

`conda activate ml_env`

## Deploying the endpoint

To run the app that creates an endpoint with the model trained on Databricks, run the following command inside the environment created by conda:

`python app.py`

The URL where data can be posted is "http://127.0.0.1:5000/predict". The data posted to the endpoint should contain the following keys: 

`['id', 'Loan Amount', 'Term', 'State', 'Annual Income', 'Income Verification Status', 
 'Average Account Balance', 'Due Amount', 'Home Ownership', 'Loan Purpose', 'Due Settlement',
 'Installment Amount', 'Payment Plan']` 

- *Note 1:* Input validation is not yet implemented.
- *Note 2:* The predictions realized by the endpoint are being stored in a local file called *predictions_log.json*. On a real world scenario they should be stored in a proper way in a database or storage for a proper monitoring of model and feature drifts. The log contains the timestamp of the predictions, the id of the loan application and the predicted value.


# Sending requests

With the endpoint running, the following script will send data to the endpoint and retrieve the predictions:

`python test.py`

