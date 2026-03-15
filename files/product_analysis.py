"""
product_analysis.py
-------------------
Step 3 – Product Utilization Analysis
Key finding: 3-product cliff — 82.71% churn at 3 products, 100% at 4.
"""

import pandas as pd
import numpy as np


def product_churn_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("NumOfProducts")["Exited"]
        .agg(Total="count", Churned="sum")
        .assign(
            ChurnRate=lambda x: (x["Churned"] / x["Total"] * 100).round(2),
            RetentionRate=lambda x: 100 - (x["Churned"] / x["Total"] * 100).round(2),
        )
        .reset_index()
    )


def single_vs_multi_retention(df: pd.DataFrame) -> dict:
    single = df[df["NumOfProducts"] == 1]["Exited"].mean()
    multi  = df[df["NumOfProducts"] == 2]["Exited"].mean()
    high   = df[df["NumOfProducts"] >= 3]["Exited"].mean()
    return {
        "single_product_churn":     round(single * 100, 2),
        "two_product_churn":        round(multi  * 100, 2),
        "three_plus_product_churn": round(high   * 100, 2),
        "retention_lift_1_to_2":    round((single - multi) * 100, 2),
    }


def product_depth_index(df: pd.DataFrame) -> float:
    retained_avg = df[df["Exited"] == 0]["NumOfProducts"].mean()
    churned_avg  = df[df["Exited"] == 1]["NumOfProducts"].mean()
    pdi = retained_avg / churned_avg if churned_avg > 0 else np.nan
    return round(pdi, 3)


def credit_card_stickiness(df: pd.DataFrame) -> dict:
    card    = df[df["HasCrCard"] == 1]["Exited"].mean()
    no_card = df[df["HasCrCard"] == 0]["Exited"].mean()
    return {
        "card_holder_churn":  round(card    * 100, 2),
        "no_card_churn":      round(no_card * 100, 2),
        "stickiness_score":   round((no_card - card) * 100, 2),
        "card_holder_count":  int((df["HasCrCard"] == 1).sum()),
        "no_card_count":      int((df["HasCrCard"] == 0).sum()),
    }


def product_mix_by_geography(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["Geography", "Exited"])["NumOfProducts"]
        .mean().round(2).reset_index()
        .rename(columns={"NumOfProducts": "AvgProducts", "Exited": "Churned"})
    )


def product_churn_heatmap_data(df: pd.DataFrame) -> pd.DataFrame:
    pivot = (
        df.groupby(["NumOfProducts", "IsActiveMember"])["Exited"]
        .mean().mul(100).round(2).reset_index()
        .pivot(index="NumOfProducts", columns="IsActiveMember", values="Exited")
        .rename(columns={0: "Inactive", 1: "Active"})
    )
    return pivot


def geography_churn_summary(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Geography")["Exited"]
        .agg(Total="count", Churned="sum")
        .assign(ChurnRate=lambda x: (x["Churned"] / x["Total"] * 100).round(2))
        .reset_index()
        .sort_values("ChurnRate", ascending=False)
    )
