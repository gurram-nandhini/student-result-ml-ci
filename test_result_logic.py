import unittest

from result_logic import predict_result


class TestPredictResult(unittest.TestCase):

    def test_pass(self):
        self.assertEqual(
            predict_result(80, 90),
            "Pass",
        )

    def test_fail_low_marks(self):
        self.assertEqual(
            predict_result(30, 90),
            "Fail",
        )

    def test_fail_low_attendance(self):
        self.assertEqual(
            predict_result(80, 60),
            "Fail",
        )

    def test_fail_both(self):
        self.assertEqual(
            predict_result(30, 60),
            "Fail",
        )


if __name__ == "__main__":
    unittest.main()
