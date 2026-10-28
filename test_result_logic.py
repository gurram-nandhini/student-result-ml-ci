import unittest
from result_logic import predict_result

class TestPredictResult(unittest.TestCase):

```
def test_student_passes(self):
    self.assertEqual(predict_result(80, 90), "Pass")

def test_low_marks(self):
    self.assertEqual(predict_result(30, 90), "Fail")

def test_low_attendance(self):
    self.assertEqual(predict_result(80, 60), "Fail")

def test_both_below_requirement(self):
    self.assertEqual(predict_result(30, 60), "Fail")

def test_invalid_marks(self):
    with self.assertRaises(ValueError):
        predict_result(110, 90)

def test_invalid_attendance(self):
    with self.assertRaises(ValueError):
        predict_result(80, -5)
```

if **name** == "**main**":
unittest.main()
