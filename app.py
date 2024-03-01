import json
import mlflow.pyfunc
import pandas as pd

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)


def predict_row(row, model):
    """Apply the model to a given row of the dataframe."""
    prediction = model.predict(pd.DataFrame(row).T)
    return prediction[0]


def predict(data: dict):
    """Predict loans on the input passed on the request."""
    local_model_path = "./mlflow_model/"
    loaded_model = mlflow.pyfunc.load_model(local_model_path)
    df = pd.read_json(data)
    ids = df.pop("id")
    prediction = df.apply(predict_row, axis=1, args=(loaded_model,))
    df["prediction"] = df.apply(predict_row, axis=1, args=(loaded_model,))
    merged_df = pd.merge(ids, df, left_index=True, right_index=True)
    predictions_df = merged_df[["id", "prediction"]]
    return predictions_df


def save_prediction(log_data: dict):
    """Save predictions to a json file locally. Could be sending to some storage or database."""
    with open("predictions_log.json", "a") as log_file:
        json.dump(log_data, log_file)
        log_file.write("\n")


@app.route("/predict", methods=["POST"])
def get_prediction():
    """Simple prediction endpoint for the vanilla model trained on Databricks and stored locally."""
    data = request.get_json()

    if "data" not in data:
        return jsonify({"Error": 'Invalid request. Missing the "data" field.'}), 400

    input_data = data["data"]
    predictions_df = predict(input_data)

    for _, row in predictions_df.iterrows():
        log_data = {
            "timestamp": str(datetime.utcnow()),
            "id": str(row["id"]),
            "prediction_result": str(row["prediction"]),
        }
        save_prediction(log_data)

    return predictions_df.reset_index().to_json(orient="records")


if __name__ == "__main__":
    # app.run(debug=True)
    app.run()
