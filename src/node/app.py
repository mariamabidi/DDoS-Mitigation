import os
from flask import Flask, request, jsonify
from joblib import load
import pandas as pd
import requests

app = Flask(__name__)

# Load model and expected features
model, expected_features = load(os.path.join("shared", "ddos_model.joblib"))

COORDINATOR_URL = "http://coordinator:5001/report"

@app.route('/analyze', methods=['POST'])
def analyze_traffic():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    try:
        # Make sure all expected features are present
        missing = [f for f in expected_features if f not in data]
        if missing:
            return jsonify({"error": f"Missing features: {missing}"}), 400

        # Construct input in correct order
        row = [data[feature] for feature in expected_features]
        traffic_df = pd.DataFrame([row], columns=expected_features)

        # Predict
        prediction = model.predict(traffic_df)[0]
        source_ip = data.get("source", "unknown")

        if prediction == 1:
            print(f"[!] DDoS detected from {source_ip}, reporting to coordinator...")
            try:
                requests.post(COORDINATOR_URL, json={"source_ip": source_ip})
            except Exception as report_error:
                print(f"❌ Failed to report to coordinator: {report_error}")
        else:
            print(f"[+] Normal traffic from {source_ip}")

        return jsonify({"prediction": int(prediction)})

    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
