def predict_result(internal_marks, attendance):
if internal_marks >= 40 and attendance >= 75:
return "PASS"
return "FAIL"

if **name** == "**main**":
result = predict_result(70, 85)
print("Predicted Result:", result)
