"""
financial_analysis.py
---------------------
Step 4 – Financial Commitment vs Engagement Analysis
Balance range: €0–€250,898 | Zero balances: 3,617 (36.2%)
"""

import pandas as pd
import numpy as np


def add_balance_segment(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    bins   = [-1, 0, 50_000, 100_000, 175_000, df["Balance"].max() + 1]
    labels = ["Zero Balance", "Low (1–50K)", "Medium (50–100K)",
              "High (100–175K)", "Premium (175K+)"]
    df["BalanceSegment"] = pd.cut(df["Balance"], bins=bins, labels=labels)
    return df


def balance_activity_churn_matrix(df: pd.DataFrame) -> pd.DataFrame:
    df = add_balance_segment(df)
    matrix = (
        df.groupby(["BalanceSegment", "IsActiveMember"], observed=True)["Exited"]
        .agg(Total="count", Churned="sum")
        .assign(ChurnRate=lambda x: (x["Churned"] / x["Total"] * 100).round(2))
        .reset_index()
    )
    matrix["Activity"] = matrix["IsActiveMember"].map({1: "Active", 0: "Inactive"})
    return matrix


def salary_balance_mismatch(df: pd.DataFrame) -> pd.DataFrame:
    salary_threshold = df["EstimatedSalary"].quantile(0.75)
    mismatch = df[(df["EstimatedSalary"] >= salary_threshold) & (df["Balance"] == 0)].copy()
    mismatch["MismatchRisk"] = "High Salary – Zero Balance"
    matched  = df[~df.index.isin(mismatch.index)].copy()
    matched["MismatchRisk"] = "Normal"
    return pd.concat([mismatch, matched], ignore_index=True)


def mismatch_churn_summary(df: pd.DataFrame) -> pd.DataFrame:
    df = salary_balance_mismatch(df)
    return (
        df.groupby("MismatchRisk")["Exited"]
        .agg(Total="count", Churned="sum")
        .assign(ChurnRate=lambda x: (x["Churned"] / x["Total"] * 100).round(2))
        .reset_index()
    )


def identify_at_risk_premium(
    df: pd.DataFrame,
    balance_percentile: float = 0.75,
    salary_percentile:  float = 0.50,
) -> pd.DataFrame:
    bal_threshold = df["Balance"].quantile(balance_percentile)
    sal_threshold = df["EstimatedSalary"].quantile(salary_percentile)
    mask = (
        (df["Balance"]         >= bal_threshold) &
        (df["EstimatedSalary"] >= sal_threshold) &
        (df["IsActiveMember"]  == 0)
    )
    at_risk = df[mask].copy()
    at_risk["RiskLabel"] = "At-Risk Premium"
    return at_risk


def high_balance_disengagement_rate(df: pd.DataFrame) -> dict:
    threshold    = df["Balance"].quantile(0.75)
    high_bal     = df[df["Balance"] >= threshold]
    inactive_pct = (high_bal["IsActiveMember"] == 0).mean() * 100
    churn_rate   = high_bal["Exited"].mean() * 100
    return {
        "high_balance_threshold": round(threshold, 2),
        "high_balance_count":     len(high_bal),
        "inactive_pct":           round(inactive_pct, 2),
        "churn_rate":             round(churn_rate, 2),
    }


def balance_churn_by_geography(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["Geography", "Exited"])["Balance"]
        .mean().round(2).reset_index()
        .rename(columns={"Balance": "AvgBalance", "Exited": "Churned"})
    )


def credit_score_segment_churn(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["CreditBand"] = pd.cut(
        df["CreditScore"],
        bins=[349, 500, 600, 700, 800, 851],
        labels=["Very Poor (350-500)", "Fair (501-600)",
                "Good (601-700)", "Very Good (701-800)", "Excellent (801-850)"],
    )
    return (
        df.groupby("CreditBand", observed=True)["Exited"]
        .agg(Total="count", Churned="sum")
        .assign(ChurnRate=lambda x: (x["Churned"] / x["Total"] * 100).round(2))
        .reset_index()
    )
