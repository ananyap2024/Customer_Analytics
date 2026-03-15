"""
retention.py
------------
Step 5 – Retention Strength Assessment
Sticky = Active + exactly 2 products + Credit Card + 3yr+ tenure
"""

import pandas as pd
import numpy as np


def define_sticky_customers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["IsSticky"] = (
        (df["IsActiveMember"] == 1) &
        (df["NumOfProducts"]  == 2) &
        (df["HasCrCard"]      == 1) &
        (df["Tenure"]         >= 3)
    ).astype(int)
    return df


def sticky_vs_non_sticky_churn(df: pd.DataFrame) -> dict:
    df = define_sticky_customers(df)
    sticky     = df[df["IsSticky"] == 1]["Exited"].mean()
    non_sticky = df[df["IsSticky"] == 0]["Exited"].mean()
    return {
        "sticky_count":          int((df["IsSticky"] == 1).sum()),
        "non_sticky_count":      int((df["IsSticky"] == 0).sum()),
        "sticky_churn_rate":     round(sticky     * 100, 2),
        "non_sticky_churn_rate": round(non_sticky * 100, 2),
        "retention_advantage":   round((non_sticky - sticky) * 100, 2),
    }


def relationship_strength_index(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    prod_score = np.where(df["NumOfProducts"] == 2, 20,
                 np.where(df["NumOfProducts"] == 1, 0, -10))
    prod_score = np.clip(prod_score, 0, 40)
    df["RSI"] = (
        df["IsActiveMember"] * 30
        + df["HasCrCard"]    * 15
        + prod_score
        + np.clip(df["Tenure"] / 10 * 15, 0, 15)
    ).astype(int)
    df["RSI_Tier"] = pd.cut(
        df["RSI"], bins=[-1, 20, 45, 70, 100],
        labels=["Weak", "Developing", "Strong", "Champion"],
    )
    return df


def rsi_churn_summary(df: pd.DataFrame) -> pd.DataFrame:
    df = relationship_strength_index(df)
    return (
        df.groupby("RSI_Tier", observed=True)["Exited"]
        .agg(Total="count", Churned="sum")
        .assign(
            ChurnRate=lambda x: (x["Churned"] / x["Total"] * 100).round(2),
            RetentionRate=lambda x: 100 - (x["Churned"] / x["Total"] * 100).round(2),
        )
        .reset_index()
    )


def engagement_tier_stability(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["EngagementTier"] = pd.cut(
        df["RelationshipScore"], bins=[-1, 20, 40, 60, 80, 100],
        labels=["Very Low (0-20)", "Low (21-40)", "Medium (41-60)",
                "High (61-80)", "Very High (81-100)"],
    )
    return (
        df.groupby("EngagementTier", observed=True)["Exited"]
        .agg(Total="count", Churned="sum")
        .assign(
            ChurnRate=lambda x: (x["Churned"] / x["Total"] * 100).round(2),
            RetentionRate=lambda x: 100 - (x["Churned"] / x["Total"] * 100).round(2),
        )
        .reset_index()
    )


def engagement_threshold_analysis(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for threshold in range(0, 100, 5):
        above = df[df["RelationshipScore"] >= threshold]
        below = df[df["RelationshipScore"] <  threshold]
        rows.append({
            "Threshold":       threshold,
            "Above_ChurnRate": round(above["Exited"].mean() * 100, 2) if len(above) else np.nan,
            "Below_ChurnRate": round(below["Exited"].mean() * 100, 2) if len(below) else np.nan,
            "Above_Count":     len(above),
        })
    return pd.DataFrame(rows)
