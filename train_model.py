import pandas as pd
import joblib
import json

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# ---------------------------------------
# 1. Create Student Dataset
# ---------------------------------------

data = {
    "study_hours": [
        8, 7, 6, 9, 5,
        2, 3, 1, 4, 2,
        9, 8, 7, 6, 5,
        1, 2, 3, 4, 2,
        10, 9, 8, 7, 6,
        1, 3, 2, 4, 3,
        9, 8, 7, 6, 5,
        2, 1, 3, 2, 4,
        10, 9, 8, 7, 6,
        1, 2, 3, 4, 2
    ],
    "attendance": [
        95, 90, 85, 98, 80,
        60, 65, 55, 70, 62,
        96, 92, 88, 84, 82,
        50, 58, 65, 72, 60,
        99, 95, 91, 89, 86,
        55, 62, 59, 75, 68,
        94, 90, 87, 83, 81,
        52, 57, 66, 71, 64,
        98, 94, 90, 88, 85,
        48, 56, 63, 69, 61
    ],
    "result": [
        1, 1, 1, 1, 1,
        0, 0, 0, 0, 0,
        1, 1, 1, 1, 1,
        0, 0, 0, 0, 0,
        1, 1, 1, 1, 1,
        0, 0, 0, 0, 0,
        1, 1, 1, 1, 1,
        0, 0, 0, 0, 0,
        1, 1, 1, 1, 1,
        0, 0, 0, 0, 0
    ]
}

df = pd.DataFrame(data)

# Save demonstration dataset
df.to_csv("student_results.csv", index=False)

print("Student dataset created.")
print(df.head())


# ---------------------------------------
# 2. Prepare Features and Target
# ---------------------------------------

X = df[["study_hours", "attendance"]]
y = df["result"]


# ---------------------------------------
# 3. Split Dataset
# ---------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ---------------------------------------
# 4. Train Model
# ---------------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)


# ---------------------------------------
# 5. Evaluate Model
# ---------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)


# ---------------------------------------
# 6. Save Model
# ---------------------------------------

joblib.dump(model, "student_result_model.pkl")

print("Model saved as student_result_model.pkl")


# ---------------------------------------
# 7. Save Metrics
# ---------------------------------------

metrics = {
    "accuracy": float(accuracy),
    "training_records": len(X_train),
    "testing_records": len(X_test)
}

with open("metrics.json", "w") as file:
    json.dump(metrics, file, indent=4)

print("Metrics saved to metrics.json")

print("Training completed successfully.")
