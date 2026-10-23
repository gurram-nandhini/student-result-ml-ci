import joblib
import pandas as pd
from pathlib import Path
from flask import Flask, jsonify, request

app = Flask(**name**)

MODEL_PATH = Path("models/ckd_pipeline.joblib")
model_bundle = None

def load_model():
global model_bundle

```
if model_bundle is None:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. "
            "Run train_model.py first."
        )

    model_bundle = joblib.load(MODEL_PATH)

return model_bundle
```

@app.get("/")
def home():
return jsonify({
"status": "ok",
"service": "CKD Prediction API"
})

@app.get("/health")
def health():
try:
load_model()
return jsonify({
"status": "healthy",
"model_loaded": True
})
except FileNotFoundError:
return jsonify({
"status": "unhealthy",
"error": "Model file not found"
}), 503

@app.post("/predict")
def predict():
data = request.get_json(silent=True)

```
if not isinstance(data, dict):
    return jsonify({
        "error": "A JSON request body is required"
    }), 400

try:
    bundle = load_model()
    feature_names = bundle["feature_names"]
    pipeline = bundle["pipeline"]

    missing_fields = [
        name for name in feature_names
        if name not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields
        }), 400

    sample = pd.DataFrame(
        [{name: data[name] for name in feature_names}],
        columns=feature_names
    )

    prediction_code = int(pipeline.predict(sample)[0])
    prediction = "CKD" if prediction_code == 1 else "NOT CKD"

    return jsonify({
        "prediction": prediction,
        "prediction_code": prediction_code,
        "model_name": bundle.get("model_name", "CKD Prediction Model"),
        "model_version": bundle.get("model_version", "1.0.0")
    })

except FileNotFoundError:
    return jsonify({
        "error": "Model not found. Train the model first."
    }), 503
except (TypeError, ValueError) as exc:
    return jsonify({
        "error": "Invalid input data",
        "details": str(exc)
    }), 400
```

if **name** == "**main**":
app.run(host="0.0.0.0", port=5000)
