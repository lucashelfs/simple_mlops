import pandas as pd
import requests

# Using the test DataFrame locally for testing the API
df = pd.read_csv("Test.csv")
df.pop("Approve Loan")
data = df.to_json(orient="records")

# The prediction URL is the flask default on localhost
url = "http://127.0.0.1:5000/predict"

# Send a POST request to the endpoint with test data in a json
response = requests.post(url, json={"data": data})

# Check the response status and content
if response.status_code == 200:
    print("Prediction successful!")
    print("Response JSON:", pd.DataFrame(response.json(), columns=["id", "prediction"]))
else:
    print("Prediction failed. Status code:", response.status_code)
