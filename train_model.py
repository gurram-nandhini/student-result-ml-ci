import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def train_model():
    data = pd.read_csv("student_data.csv")

    features = ["marks", "attendance", "study_hours"]
    X = data[features]
    y = data["passed"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    joblib.dump(model, "student_result_model.joblib")

    print(f"Model accuracy: {accuracy:.2f}")
    print("Model saved to student_result_model.joblib")

    return accuracy


if __name__ == "__main__":
    train_model()
