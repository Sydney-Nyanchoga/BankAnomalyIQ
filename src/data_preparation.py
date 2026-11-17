import pandas as pd
import numpy as np
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset location
DATA_PATH = BASE_DIR / "data" / "raw" / "bank_transactions_data_2.csv"

# Load dataset
df = pd.read_csv(DATA_PATH)

print("\n========== DATASET OVERVIEW ==========")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== DUPLICATES ==========")
print(f"Duplicate rows: {df.duplicated().sum()}")

# Convert transaction dates
df["TransactionDate"] = pd.to_datetime(
    df["TransactionDate"], errors="coerce"
)

df["PreviousTransactionDate"] = pd.to_datetime(
    df["PreviousTransactionDate"], errors="coerce"
)

# Feature engineering
df["TransactionHour"] = df["TransactionDate"].dt.hour
df["TransactionDay"] = df["TransactionDate"].dt.day_name()
df["TransactionMonth"] = df["TransactionDate"].dt.month

# Transaction amount relative to account balance
df["AmountBalanceRatio"] = (
    df["TransactionAmount"] /
    df["AccountBalance"].replace(0, np.nan)
)

# Account behavioural features
account_stats = df.groupby("AccountID").agg(
    AccountTransactionCount=("TransactionID", "count"),
    AccountAverageAmount=("TransactionAmount", "mean"),
    AccountMaximumAmount=("TransactionAmount", "max"),
    AccountAmountStd=("TransactionAmount", "std"),
    UniqueDevices=("DeviceID", "nunique"),
    UniqueIPs=("IP Address", "nunique"),
    ChannelDiversity=("Channel", "nunique")
).reset_index()

df = df.merge(account_stats, on="AccountID", how="left")

# Relative transaction amount
df["AmountVsAccountAverage"] = (
    df["TransactionAmount"] /
    df["AccountAverageAmount"].replace(0, np.nan)
)

# Check inconsistent dates
invalid_dates = (
    df["PreviousTransactionDate"] > df["TransactionDate"]
).sum()

print("\n========== DATE QUALITY CHECK ==========")
print(f"Previous dates later than transaction dates: {invalid_dates}")

# Save prepared dataset
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = OUTPUT_DIR / "prepared_transactions.csv"
df.to_csv(OUTPUT_PATH, index=False)

print("\n========== COMPLETE ==========")
print(f"Prepared dataset saved to: {OUTPUT_PATH}")
print(f"Final shape: {df.shape}")
