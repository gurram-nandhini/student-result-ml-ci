import unittest

from result_logic import predict_result


class TestResultLogic(unittest.TestCase):

    def test_pass_case(self):
        self.assertEqual(predict_result(85, 75), "Pass")

    def test_fail_due_to_attendance(self):
        self.assertEqual(predict_result(60, 80), "Fail")

    def test_fail_due_to_marks(self):
        self.assertEqual(predict_result(90, 30), "Fail")

    def test_minimum_attendance_and_marks(self):
        self.assertEqual(predict_result(75, 40), "Pass")


if __name__ == "__main__":
    unittest.main()
