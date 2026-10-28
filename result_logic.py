def predict_result(marks, attendance):
if marks < 40:
return "Fail"
elif attendance < 75:
return "Fail"
else:
return "Pass"
