import unittest
import os
import joblib


class TestMLPipeline(unittest.TestCase):

    def test_model_file_exists(self):
        self.assertTrue(
            os.path.exists("student_result_model.pkl"),
            "Model file was not created"
        )

    def test_metrics_file_exists(self):
        self.assertTrue(
            os.path.exists("metrics.json"),
            "Metrics file was not created"
        )

    def test_dataset_file_exists(self):
        self.assertTrue(
            os.path.exists("student_results.csv"),
            "Dataset file was not created"
        )

    def test_model_can_predict(self):
        model = joblib.load("student_result_model.pkl")

        prediction = model.predict([[8, 90]])

        self.assertEqual(len(prediction), 1)


if __name__ == "__main__":
    unittest.main()
