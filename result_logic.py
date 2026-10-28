def predict_result(marks, attendance):
if not isinstance(marks, (int, float)):
raise ValueError("Marks must be a number.")

```
if not isinstance(attendance, (int, float)):
    raise ValueError("Attendance must be a number.")

if not 0 <= marks <= 100:
    raise ValueError("Marks must be between 0 and 100.")

if not 0 <= attendance <= 100:
    raise ValueError("Attendance must be between 0 and 100.")

if marks < 40 or attendance < 75:
    return "Fail"

return "Pass"
```
