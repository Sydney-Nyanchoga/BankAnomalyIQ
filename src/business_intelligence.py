
import pandas as pd
from pathlib import Path


# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR / "data" / "processed" / "scored_transactions.csv"
)

OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MERCHANT_OUTPUT = OUTPUT_DIR / "merchant_intelligence.csv"
CHANNEL_OUTPUT = OUTPUT_DIR / "channel_intelligence.csv"


# ==========================================
# 2. LOAD SCORED TRANSACTIONS
# ==========================================

print("\nLoading scored transaction data...")

df = pd.read_csv(DATA_PATH)

required_columns = [
    "TransactionID",
    "AccountID",
    "MerchantID",
    "Channel",
    "TransactionAmount",
    "TransactionDuration",
    "LoginAttempts",
    "AnomalyFlag",
    "AnomalyScore"
]

missing = [
    column for column in required_columns
    if column not in df.columns
]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

print(f"Loaded {len(df):,} transactions.")


# ==========================================
# 3. MERCHANT INTELLIGENCE
# ==========================================

print("\nAnalysing merchant activity...")

merchant = (
    df.groupby("MerchantID")
    .agg(
        TransactionCount=("TransactionID", "count"),
        UniqueAccounts=("AccountID", "nunique"),
        TotalTransactionValue=("TransactionAmount", "sum"),
        AverageTransactionValue=("TransactionAmount", "mean"),
        MedianTransactionValue=("TransactionAmount", "median"),
        MaximumTransactionValue=("TransactionAmount", "max"),
        ChannelDiversity=("Channel", "nunique"),
        AnomalyCount=(
            "AnomalyFlag",
            lambda x: (x == "Anomaly").sum()
        ),
        AverageAnomalyScore=("AnomalyScore", "mean")
    )
    .reset_index()
)

# Calculate merchant-level anomaly rate
merchant["AnomalyRatePct"] = (
    merchant["AnomalyCount"] /
    merchant["TransactionCount"] * 100
).round(2)

# Share of total transaction volume
merchant["TransactionSharePct"] = (
    merchant["TransactionCount"] /
    len(df) * 100
).round(2)

# Share of total transaction value
total_value = df["TransactionAmount"].sum()

merchant["ValueSharePct"] = (
    merchant["TotalTransactionValue"] /
    total_value * 100
).round(2)

# Avoid ranking merchants with very few observations
merchant["ReviewRankingEligible"] = (
    merchant["TransactionCount"] >= 5
)

merchant = merchant.sort_values(
    ["ReviewRankingEligible", "AnomalyRatePct", "AnomalyCount"],
    ascending=[False, False, False]
)

merchant.to_csv(MERCHANT_OUTPUT, index=False)


# ==========================================
# 4. CHANNEL INTELLIGENCE
# ==========================================

print("\nAnalysing banking channel activity...")

channel = (
    df.groupby("Channel")
    .agg(
        TransactionCount=("TransactionID", "count"),
        UniqueAccounts=("AccountID", "nunique"),
        UniqueMerchants=("MerchantID", "nunique"),
        TotalTransactionValue=("TransactionAmount", "sum"),
        AverageTransactionValue=("TransactionAmount", "mean"),
        MedianTransactionValue=("TransactionAmount", "median"),
        AverageTransactionDuration=("TransactionDuration", "mean"),
        AverageLoginAttempts=("LoginAttempts", "mean"),
        AnomalyCount=(
            "AnomalyFlag",
            lambda x: (x == "Anomaly").sum()
        ),
        AverageAnomalyScore=("AnomalyScore", "mean")
    )
    .reset_index()
)

channel["TransactionSharePct"] = (
    channel["TransactionCount"] /
    len(df) * 100
).round(2)

channel["ValueSharePct"] = (
    channel["TotalTransactionValue"] /
    total_value * 100
).round(2)

# Percentage of transactions within each channel flagged as anomalies
channel["AnomalyRatePct"] = (
    channel["AnomalyCount"] /
    channel["TransactionCount"] * 100
).round(2)

# How much each channel contributes to all flagged anomalies
total_anomalies = (
    df["AnomalyFlag"] == "Anomaly"
).sum()

if total_anomalies > 0:
    channel["ShareOfAllAnomaliesPct"] = (
        channel["AnomalyCount"] /
        total_anomalies * 100
    ).round(2)
else:
    channel["ShareOfAllAnomaliesPct"] = 0

channel = channel.sort_values(
    "TransactionCount",
    ascending=False
)

channel.to_csv(CHANNEL_OUTPUT, index=False)


# ==========================================
# 5. DISPLAY RESULTS
# ==========================================

print("\n====================================")
print(" MERCHANT INTELLIGENCE SUMMARY")
print("====================================")

print(f"Merchants analysed: {len(merchant)}")
print("\nTop merchants by anomaly rate (minimum 5 transactions):")

print(
    merchant.loc[
        merchant["ReviewRankingEligible"]
    ][
        [
            "MerchantID",
            "TransactionCount",
            "UniqueAccounts",
            "AnomalyCount",
            "AnomalyRatePct"
        ]
    ].head(10).to_string(index=False)
)


print("\n====================================")
print(" CHANNEL INTELLIGENCE SUMMARY")
print("====================================")

print(
    channel[
        [
            "Channel",
            "TransactionCount",
            "TransactionSharePct",
            "AverageTransactionValue",
            "AnomalyCount",
            "AnomalyRatePct"
        ]
    ].to_string(index=False)
)


print("\n====================================")
print(" OUTPUT FILES")
print("====================================")

print(f"Merchant analysis: {MERCHANT_OUTPUT}")
print(f"Channel analysis: {CHANNEL_OUTPUT}")

print("\nBusiness intelligence analysis completed!")
