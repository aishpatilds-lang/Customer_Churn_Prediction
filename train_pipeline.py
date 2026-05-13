import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

# ---------------- LOAD DATA ----------------
df = pd.read_csv("telecom_churn_data.csv")

# Clean TotalCharges
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna()

# Target
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

# ---------------- SELECT FEATURES ----------------
features = [
    "tenure",
    "MonthlyCharges",
    "Contract",
    "InternetService",
    "PaymentMethod",
    "TechSupport",
    "OnlineSecurity"
]

X = df[features]
y = df["Churn"]

# ---------------- SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------- PIPELINE ----------------
cat_cols = ["Contract", "InternetService", "PaymentMethod", "TechSupport", "OnlineSecurity"]
num_cols = ["tenure", "MonthlyCharges"]

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
])

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", RandomForestClassifier(n_estimators=100))
])

# ---------------- TRAIN ----------------
pipeline.fit(X_train, y_train)

# ---------------- SAVE ----------------
pickle.dump(pipeline, open("pipeline.pkl", "wb"))

print("✅ pipeline.pkl created successfully!")