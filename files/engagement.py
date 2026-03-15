"""
engagement.py
-------------
Step 2 – Engagement Classification
4 profiles + ERR KPI + gender, age, tenure breakdowns.
"""

import pandas as pd
import numpy as np

ACTIVE_ENGAGED        = "Active Engaged"
INACTIVE_DISENGAGED   = "Inactive Disengaged"
ACTIVE_LOW_PRODUCT    = "Active Low-Product"
INACTIVE_HIGH_BALANCE = "Inactive High-Balance"

_BALANCE_HIGH_THRESHOLD = 75_000
_PRODUCT_HIGH_THRESHOLD = 2


def classify_engagement(
    df: pd.DataFrame,
    balance_threshold: float = _BALANCE_HIGH_THRESHOLD,
    product_threshold: int   = _PRODUCT_HIGH_THRESHOLD,
) -> pd.DataFrame:
    df = df.copy()
    conditions = [
        (df["IsActiveMember"] == 1) & (df["NumOfProducts"] >= product_threshold),
        (df["IsActiveMember"] == 0) & (df["NumOfProducts"] < product_threshold) & (df["Balance"] < balance_threshold),
        (df["IsActiveMember"] == 1) & (df["NumOfProducts"] < product_threshold),
        (df["IsActiveMember"] == 0) & (df["Balance"] >= balance_threshold),
    ]
    choices = [ACTIVE_ENGAGED, INACTIVE_DISENGAGED, ACTIVE_LOW_PRODUCT, INACTIVE_HIGH_BALANCE]
    df["EngagementProfile"] = np.select(conditions, choices, default=INACTIVE_DISENGAGED)
    df["RelationshipScore"] = (
        df["IsActiveMember"] * 30
        + df["HasCrCard"]    * 15
        + np.clip((df["NumOfProducts"] - 1) * 20, 0, 40)
        + np.clip(df["Tenure"] / 10 * 15, 0, 15)
    ).astype(int)
    return df


def engagement_retention_ratio(df: pd.DataFrame) -> dict:
    active   = df[df["IsActiveMember"] == 1]["Exited"].mean()
    inactive = df[df["IsActiveMember"] == 0]["Exited"].mean()
    ratio    = inactive / active if active > 0 else np.nan
    return {
        "active_churn_rate":   round(active   * 100, 2),
        "inactive_churn_rate": round(inactive * 100, 2),
        "ratio":               round(ratio, 2),
    }


def profile_churn_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("EngagementProfile")["Exited"]
        .agg(Total="count", Churned="sum")
        .assign(ChurnRate=lambda x: (x["Churned"] / x["Total"] * 100).round(2))
        .reset_index()
        .sort_values("ChurnRate", ascending=False)
    )


def tenure_churn_summary(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["TenureBucket"] = pd.cut(
        df["Tenure"], bins=[-1, 1, 3, 5, 7, 10],
        labels=["0-1 yr", "2-3 yr", "4-5 yr", "6-7 yr", "8-10 yr"],
    )
    return (
        df.groupby("TenureBucket", observed=True)["Exited"]
        .agg(Total="count", Churned="sum")
        .assign(ChurnRate=lambda x: (x["Churned"] / x["Total"] * 100).round(2))
        .reset_index()
    )


def gender_churn_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Gender")["Exited"]
        .agg(Total="count", Churned="sum")
        .assign(ChurnRate=lambda x: (x["Churned"] / x["Total"] * 100).round(2))
        .reset_index()
    )


def age_group_churn(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["AgeGroup"] = pd.cut(
        df["Age"], bins=[17, 25, 35, 45, 55, 65, 92],
        labels=["18-25", "26-35", "36-45", "46-55", "56-65", "66+"],
    )
    return (
        df.groupby("AgeGroup", observed=True)["Exited"]
        .agg(Total="count", Churned="sum")
        .assign(ChurnRate=lambda x: (x["Churned"] / x["Total"] * 100).round(2))
        .reset_index()
    )
