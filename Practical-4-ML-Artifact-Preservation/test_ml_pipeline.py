import json
import os
import unittest

import joblib
import pandas as pd

from train_model import create_dataset, train_model


class TestMLPipeline(unittest.TestCase):

    def test_dataset_created(self):
        data = create_dataset()
        self.assertIsInstance(data, pd.DataFrame)

    def test_dataset_has_300_records(self):
        data = create_dataset()
        self.assertEqual(len(data), 300)

    def test_dataset_has_required_columns(self):
        data = create_dataset()

        required_columns = [
            "attendance",
            "internal_marks",
            "assignment_marks",
            "previous_score",
            "weighted_score",
            "result",
        ]

        for column in required_columns:
            self.assertIn(column, data.columns)

    def test_model_training_creates_files(self):
        train_model()

        self.assertTrue(os.path.exists("student_results.csv"))
        self.assertTrue(os.path.exists("student_result_model.pkl"))
        self.assertTrue(os.path.exists("metrics.json"))

    def test_metrics_accuracy_passes_quality_gate(self):
        train_model()

        with open("metrics.json", "r", encoding="utf-8") as file:
            metrics = json.load(file)

        self.assertGreaterEqual(metrics["accuracy"], 0.85)

    def test_model_can_predict(self):
        train_model()

        model = joblib.load("student_result_model.pkl")

        sample = pd.DataFrame(
            [[90, 85, 80, 75]],
            columns=[
                "attendance",
                "internal_marks",
                "assignment_marks",
                "previous_score",
            ],
        )

        prediction = model.predict(sample)

        self.assertEqual(len(prediction), 1)

    def test_low_performance_student(self):
        train_model()

        model = joblib.load("student_result_model.pkl")

        sample = pd.DataFrame(
            [{
                "attendance": 55,
                "internal_marks": 30,
                "assignment_marks": 40,
                "previous_score": 35,
            }]
        )

        prediction = model.predict(sample)[0]

        self.assertEqual(int(prediction), 0)


if __name__ == "__main__":
    unittest.main()
