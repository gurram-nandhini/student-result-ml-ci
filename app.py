```python
import joblib
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

MODEL_PATH = "student_result_model.pkl"

# These feature names must match train_model.py
FEATURES = ["study_hours", "attendance"]


def load_model():
    return joblib.load(MODEL_PATH)


@app.get("/")
def home():
    return jsonify({
        "status": "ok",
        "service": "student-result-prediction"
    })


@app.get("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.post("/predict")
def predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "A JSON request body is required"
        }), 400

    missing_fields = [
        feature for feature in FEATURES
        if feature not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields
        }), 400

    try:
        sample = pd.DataFrame([{
            "study_hours": float(data["study_hours"]),
            "attendance": float(data["attendance"])
        }])

        model = load_model()
        prediction_code = int(model.predict(sample)[0])

        prediction = "PASS" if prediction_code == 1 else "FAIL"

        return jsonify({
            "prediction": prediction,
            "prediction_code": prediction_code
        })

    except (TypeError, ValueError):
        return jsonify({
            "error": "study_hours and attendance must be numeric"
        }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```
