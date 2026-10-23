import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
)

# 1. Load dataset
DATASET_PATH = "dataset/kidney_disease.csv"

df = pd.read_csv(DATASET_PATH)

# 2. Clean column names
df.columns = df.columns.str.strip().str.lower()

# 3. Remove duplicate rows
df = df.drop_duplicates().copy()

# 4. Identify target column
TARGET = "classification"

if TARGET not in df.columns:
    raise ValueError(
        f"Target column '{TARGET}' not found. "
        f"Available columns: {df.columns.tolist()}"
    )

# 5. Clean target values
df[TARGET] = (
    df[TARGET]
    .astype(str)
    .str.strip()
    .str.lower()
)

# Standardize common CKD labels
df[TARGET] = df[TARGET].replace({
    "ckd": "ckd",
    "notckd": "notckd",
    "not ckd": "notckd",
})

# Remove missing or unexpected target values
df = df[df[TARGET].isin(["ckd", "notckd"])].copy()

# 6. Separate features and target
X = df.drop(columns=[TARGET])
y = df[TARGET].map({
    "notckd": 0,
    "ckd": 1,
})

# Remove columns that contain no usable information
X = X.dropna(axis=1, how="all")

# Convert blank strings into missing values
X = X.replace(r"^\s*$", float("nan"), regex=True)

# Identify numeric and categorical columns
numeric_features = X.select_dtypes(
    include=["number"]
).columns.tolist()

categorical_features = [
    column for column in X.columns
    if column not in numeric_features
]

# 7. Create preprocessing pipelines
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])

categorical_pipeline = Pipeline([
    (
        "imputer",
        SimpleImputer(
            strategy="most_frequent"
        ),
    ),
    (
        "encoder",
        OneHotEncoder(
            handle_unknown="ignore"
        ),
    ),
])

preprocessor = ColumnTransformer([
    (
        "numeric",
        numeric_pipeline,
        numeric_features,
    ),
    (
        "categorical",
        categorical_pipeline,
        categorical_features,
    ),
])

# 8. Create the complete ML pipeline
model = Pipeline([
    ("preprocessor", preprocessor),
    (
        "classifier",
        RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            class_weight="balanced",
        ),
    ),
])

# 9. Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

# 10. Train the model
model.fit(X_train, y_train)

# 11. Make predictions
y_pred = model.predict(X_test)

# 12. Evaluate the model
accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0,
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0,
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0,
)

print("\nMODEL EVALUATION")
print("----------------")
print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    zero_division=0,
))

# 13. Save the complete pipeline
os.makedirs("models", exist_ok=True)

joblib.dump(
    {
        "pipeline": model,
        "feature_names": X.columns.tolist(),
        "metrics": {
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1_score": float(f1),
        },
        "model_name": "CKD Prediction Model",
        "model_version": "1.0.0",
    },
    "models/ckd_pipeline.joblib",
)

print("\nModel saved successfully!")
print("Location: models/ckd_pipeline.joblib")
