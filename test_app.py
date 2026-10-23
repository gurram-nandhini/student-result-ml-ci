import unittest
from unittest.mock import patch

from app import app

class TestCKDPredictionAPI(unittest.TestCase):

```
def setUp(self):
    self.client = app.test_client()

def test_home_endpoint(self):
    response = self.client.get("/")

    self.assertEqual(response.status_code, 200)
    self.assertEqual(
        response.get_json()["service"],
        "CKD Prediction API"
    )

def test_health_endpoint_without_model(self):
    with patch("app.load_model", side_effect=FileNotFoundError):
        response = self.client.get("/health")

    self.assertEqual(response.status_code, 503)
    self.assertEqual(
        response.get_json()["status"],
        "unhealthy"
    )

def test_missing_fields(self):
    bundle = {
        "feature_names": ["age", "blood_pressure"],
        "pipeline": None,
        "model_name": "CKD Prediction Model",
        "model_version": "1.0.0"
    }

    with patch("app.load_model", return_value=bundle):
        response = self.client.post(
            "/predict",
            json={"age": 50}
        )

    self.assertEqual(response.status_code, 400)
    self.assertIn(
        "missing_fields",
        response.get_json()
    )

def test_successful_prediction(self):
    bundle = {
        "feature_names": ["age", "blood_pressure"],
        "pipeline": type(
            "FakePipeline",
            (),
            {
                "predict": lambda self, data: [1]
            }
        )(),
        "model_name": "CKD Prediction Model",
        "model_version": "1.0.0"
    }

    with patch("app.load_model", return_value=bundle):
        response = self.client.post(
            "/predict",
            json={
                "age": 50,
                "blood_pressure": 80
            }
        )

    self.assertEqual(response.status_code, 200)
    self.assertEqual(
        response.get_json()["prediction"],
        "CKD"
    )
```

if **name** == "**main**":
unittest.main()
