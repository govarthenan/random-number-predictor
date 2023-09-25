from flask import Flask, jsonify, request
import tensorflow as tf
import numpy as np
from pathlib import Path
from datetime import datetime
import time


app = Flask(__name__)

# Historical data store
historical_data = []


# Prediction
@app.route("/predict", methods=["POST"])
def predict():
    """Payload format
    {"number": 1.357}

    Unix time will be automatically fetched from system.
    """

    # Get unix time from system
    unix_time = datetime.utcfromtimestamp(int(time.time()))
    hour, minute = unix_time.hour, unix_time.minute

    # Get latest number from payload
    json_ = request.json
    latest_number = float(json_["number"])

    historical_data.append([latest_number, hour, minute])  # store historical data for lookback in shape = (n, 3)
    n_lookback = 50  # time steps to look back at when predicting

    # Predict only if enough historical data is present
    if len(historical_data) >= n_lookback:
        # Prepare input data and predict
        inference_input = np.array([historical_data[-n_lookback:]])  # shape = (1, n_lookback, 1)

        pred = model.predict(inference_input)
        pred = float(pred[0][0])

        return jsonify({"prediction": pred})
    else:
        return jsonify({"prediction": None})


if __name__ == "__main__":
    # As relative filepaths might differ based on where the script is run from
    try:
        model_path = Path("../models/02-hour_min-sigmoid.keras").absolute()
        model = tf.keras.models.load_model(model_path, compile=False)
    except Exception:
        model_path = Path("./models/02-hour_min-sigmoid.keras").absolute()
        model = tf.keras.models.load_model(model_path, compile=False)
    finally:
        app.run()
