def predict_result(attendance, marks):
    """
    Predict whether a student passes or fails.

    Rules:
    - Attendance must be at least 75%.
    - Marks must be at least 40.
    """
    if attendance < 75:
        return "Fail"

    if marks < 40:
        return "Fail"

    return "Pass"
