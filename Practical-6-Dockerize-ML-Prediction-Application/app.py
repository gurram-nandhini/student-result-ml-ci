from pathlib import Path

import logging
import sys
import time
import uuid

import joblib
import pandas as pd

from flask import Flask, jsonify, request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True
)

logger = logging.getLogger("student-result-api")
logger.info("event=application_started")


# Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["endpoint"]
)


# Request logging and monitoring
@app.before_request
def log_request_start():
    request.environ["request_start_time"] = time.time()
    request.environ["request_timer"] = time.perf_counter()
    request.environ["request_id"] = str(uuid.uuid4())

    logger.info(
        "event=request_started request_id=%s method=%s path=%s",
        request.environ["request_id"],
        request.method,
        request.path
    )


@app.after_request
def log_request_end(response):
    start_time = request.environ.get(
        "request_start_time", time.time()
    )

    duration = (time.time() - start_time) * 1000

    request_id = request.environ.get(
        "request_id", "unknown"
    )

    # Prometheus request counter
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).inc()

    # Prometheus response time
    timer = request.environ.get("request_timer")

    if timer is not None:
        REQUEST_LATENCY.labels(
            endpoint=request.path
        ).observe(time.perf_counter() - timer)

    logger.info(
        "event=request_completed request_id=%s status=%s duration_ms=%.2f",
        request_id,
        response.status_code,
        duration
    )

    response.headers["X-Request-ID"] = request_id

    return response


# Model configuration
MODEL_PATH = Path("student_result_model.pkl")

FEATURES = [
    "attendance",
    "internal_marks",
    "assignment_marks",
    "previous_score"
]


# Load ML model
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "student_result_model.pkl was not found. "
            "Run the training pipeline first."
        )

    return joblib.load(MODEL_PATH)


# Home endpoint
@app.get("/")
def health_check():
    return jsonify({
        "status": "ok",
        "service": "student-result-prediction"
    })


# Health endpoint
@app.get("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


# Prometheus metrics endpoint
@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


# Prediction endpoint
@app.post("/predict")
def predict():

    request_id = request.environ.get(
        "request_id", "unknown"
    )

    try:
        data = request.get_json(silent=True)

        if not data:
            logger.warning(
                "event=invalid_request request_id=%s reason=missing_json",
                request_id
            )

            return jsonify({
                "error": "JSON request body is required"
            }), 400

        missing_fields = [
            feature for feature in FEATURES
            if feature not in data
        ]

        if missing_fields:
            logger.warning(
                "event=validation_failed request_id=%s missing_fields=%s",
                request_id,
                missing_fields
            )

            return jsonify({
                "error": "Missing required fields",
                "missing_fields": missing_fields
            }), 400

        sample = pd.DataFrame([{
            feature: data[feature]
            for feature in FEATURES
        }])

        model = load_model()

        prediction_code = int(model.predict(sample)[0])

        prediction = (
            "PASS" if prediction_code == 1 else "FAIL"
        )

        logger.info(
            "event=prediction_success request_id=%s prediction=%s",
            request_id,
            prediction
        )

        return jsonify({
            "prediction": prediction,
            "prediction_code": prediction_code
        })

    except Exception:
        logger.exception(
            "event=prediction_failed request_id=%s",
            request_id
        )

        return jsonify({
            "error": "Prediction failed"
        }), 500


# Run Flask application
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )   