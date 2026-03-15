"""
data_loader.py
--------------
Step 1 – Data Ingestion & Validation
European Bank Dataset (Year: 2025) | 10,000 customers | 14 columns | 0 missing values
"""

import pandas as pd
import numpy as np
from pathlib import Path

REQUIRED_COLUMNS = [
    "Year", "CustomerId", "Surname", "CreditScore", "Geography", "Gender",
    "Age", "Tenure", "Balance", "NumOfProducts", "HasCrCard",
    "IsActiveMember", "EstimatedSalary", "Exited",
]

BINARY_COLUMNS  = ["HasCrCard", "IsActiveMember", "Exited"]
NUMERIC_COLUMNS = ["CreditScore", "Age", "Tenure", "Balance",
                   "NumOfProducts", "EstimatedSalary"]


def load_data(filepath: str | Path) -> pd.DataFrame:
    """Load dataset from CSV and run all validation checks."""
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Dataset not found at: {filepath}")
    df = pd.read_csv(filepath)
    df = _validate_schema(df)
    df = _validate_binary_columns(df)
    df = _validate_numeric_columns(df)
    df = _validate_churn_label(df)
    df = _cast_types(df)
    return df


def _validate_schema(df):
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df[REQUIRED_COLUMNS]


def _validate_binary_columns(df):
    for col in BINARY_COLUMNS:
        unique_vals = set(df[col].dropna().unique())
        if not unique_vals.issubset({0, 1}):
            raise ValueError(f"Column '{col}' must be binary (0/1). Found: {unique_vals}")
    return df


def _validate_numeric_columns(df):
    for col in NUMERIC_COLUMNS:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())
    return df


def _validate_churn_label(df):
    churn_vals = set(df["Exited"].dropna().unique())
    if not churn_vals.issubset({0, 1}):
        raise ValueError(f"'Exited' must be binary. Found: {churn_vals}")
    return df


def _cast_types(df):
    int_cols = ["Year", "CreditScore", "Age", "Tenure", "NumOfProducts",
                "HasCrCard", "IsActiveMember", "Exited"]
    for col in int_cols:
        df[col] = df[col].astype(int)
    df["Balance"]         = df["Balance"].astype(float)
    df["EstimatedSalary"] = df["EstimatedSalary"].astype(float)
    return df


def dataset_summary(df: pd.DataFrame) -> dict:
    """Key summary statistics for dashboard header panels."""
    return {
        "total_customers":  len(df),
        "churn_count":      int(df["Exited"].sum()),
        "churn_rate":       round(df["Exited"].mean() * 100, 2),
        "active_members":   int(df["IsActiveMember"].sum()),
        "inactive_members": int((df["IsActiveMember"] == 0).sum()),
        "avg_products":     round(df["NumOfProducts"].mean(), 2),
        "avg_balance":      round(df["Balance"].mean(), 2),
        "has_credit_card":  int(df["HasCrCard"].sum()),
        "zero_balance":     int((df["Balance"] == 0).sum()),
        "geographies":      df["Geography"].value_counts().to_dict(),
        "year":             int(df["Year"].iloc[0]),
        "missing_values":   int(df.isnull().sum().sum()),
    }
