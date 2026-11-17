import pandas as pd
import numpy as np
import joblib

from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline


# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR / "data" / "processed" / "prepared_transactions.csv"
)

MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "isolation_forest.joblib"
OUTPUT_PATH = OUTPUT_DIR / "scored_transactions.csv"


# ==========================================
# 2. LOAD PREPARED DATA
# ==========================================

print("\nLoading prepared transaction data...")

df = pd.read_csv(DATA_PATH)

print(f"Dataset loaded: {df.shape[0]} transactions")


# ==========================================
# 3. SELECT MODEL FEATURES
# ==========================================

FEATURES = [
    "TransactionAmount",
    "CustomerAge",
    "TransactionDuration",
    "LoginAttempts",
    "AccountBalance",
    "TransactionHour",
    "TransactionMonth",
    "AmountBalanceRatio",
    "AccountTransactionCount",
    "AccountAverageAmount",
    "AccountMaximumAmount",
    "AccountAmountStd",
    "UniqueDevices",
    "UniqueIPs",
    "ChannelDiversity",
    "AmountVsAccountAverage"
]

# Check that all expected features exist
missing_features = [
    col for col in FEATURES if col not in df.columns
]

if missing_features:
    raise ValueError(
        f"Missing model features: {missing_features}. "
        "Run data_preparation.py first."
    )

X = df[FEATURES].copy()

# Convert any unexpected values to numeric
for column in FEATURES:
    X[column] = pd.to_numeric(
        X[column], errors="coerce"
    )

# Replace infinite values with missing values
X = X.replace([np.inf, -np.inf], np.nan)


# ==========================================
# 4. BUILD ISOLATION FOREST PIPELINE
# ==========================================

print("\nBuilding Isolation Forest model...")

model = Pipeline([
    (
        "imputer",
        SimpleImputer(strategy="median")
    ),
    (
        "isolation_forest",
        IsolationForest(
            n_estimators=200,
            contamination=0.05,
            random_state=42,
            n_jobs=-1
        )
    )
])


# ==========================================
# 5. TRAIN THE MODEL
# ==========================================

print("\nTraining anomaly detection model...")

model.fit(X)

print("Model training completed!")


# ==========================================
# 6. GENERATE ANOMALY PREDICTIONS
# ==========================================

print("\nScoring transactions...")

# Isolation Forest:
# -1 = anomaly
#  1 = normal observation

predictions = model.predict(X)

# Lower decision scores indicate more unusual records.
# Reverse the sign so higher scores mean more unusual.
raw_scores = model.named_steps[
    "isolation_forest"
].score_samples(
    model.named_steps["imputer"].transform(X)
)

df["AnomalyScore"] = -raw_scores

df["AnomalyFlag"] = np.where(
    predictions == -1,
    "Anomaly",
    "Normal"
)

# Rank transactions by anomaly score
df["AnomalyRank"] = (
    df["AnomalyScore"]
    .rank(method="min", ascending=False)
    .astype(int)
)

# Percentile: 100 means among the most unusual
df["AnomalyPercentile"] = (
    df["AnomalyScore"].rank(pct=True) * 100
).round(2)


# ==========================================
# 7. SAVE MODEL AND SCORED DATA
# ==========================================

joblib.dump(
    {
        "model": model,
        "features": FEATURES
    },
    MODEL_PATH
)

df.to_csv(OUTPUT_PATH, index=False)


# ==========================================
# 8. DISPLAY MODEL SUMMARY
# ==========================================

anomaly_count = (df["AnomalyFlag"] == "Anomaly").sum()
normal_count = (df["AnomalyFlag"] == "Normal").sum()

anomaly_percentage = (
    anomaly_count / len(df)
) * 100

print("\n====================================")
print(" ISOLATION FOREST MODEL SUMMARY")
print("====================================")

print(f"Total transactions: {len(df):,}")
print(f"Normal transactions: {normal_count:,}")
print(f"Flagged anomalies: {anomaly_count:,}")
print(f"Anomaly percentage: {anomaly_percentage:.2f}%")

print("\nTOP 10 MOST UNUSUAL TRANSACTIONS")

display_columns = [
    "TransactionID",
    "AccountID",
    "TransactionAmount",
    "TransactionType",
    "Channel",
    "LoginAttempts",
    "AnomalyScore",
    "AnomalyFlag"
]

print(
    df.sort_values(
        "AnomalyScore",
        ascending=False
    )[display_columns].head(10).to_string(index=False)
)

print("\n====================================")
print(" OUTPUT FILES CREATED")
print("====================================")

print(f"Model: {MODEL_PATH}")
print(f"Scored data: {OUTPUT_PATH}")

print("\nAnomaly detection completed successfully!")
