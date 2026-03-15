"""
kpi.py
------
Aggregates all five project KPIs into a single summary dictionary.
"""

import pandas as pd
from engagement         import engagement_retention_ratio, classify_engagement
from product_analysis   import product_depth_index, credit_card_stickiness
from financial_analysis import high_balance_disengagement_rate
from retention          import sticky_vs_non_sticky_churn, relationship_strength_index


def compute_all_kpis(df: pd.DataFrame) -> dict:
    if "EngagementProfile" not in df.columns:
        df = classify_engagement(df)
    if "RSI" not in df.columns:
        df = relationship_strength_index(df)

    err  = engagement_retention_ratio(df)
    pdi  = product_depth_index(df)
    ccs  = credit_card_stickiness(df)
    hbdr = high_balance_disengagement_rate(df)
    svns = sticky_vs_non_sticky_churn(df)

    return {
        "active_churn_pct":             err["active_churn_rate"],
        "inactive_churn_pct":           err["inactive_churn_rate"],
        "engagement_retention_ratio":   err["ratio"],
        "product_depth_index":          pdi,
        "card_holder_churn_pct":        ccs["card_holder_churn"],
        "no_card_churn_pct":            ccs["no_card_churn"],
        "credit_card_stickiness_score": ccs["stickiness_score"],
        "high_balance_inactive_pct":    hbdr["inactive_pct"],
        "high_balance_churn_pct":       hbdr["churn_rate"],
        "sticky_churn_pct":             svns["sticky_churn_rate"],
        "non_sticky_churn_pct":         svns["non_sticky_churn_rate"],
        "sticky_retention_advantage":   svns["retention_advantage"],
        "avg_rsi":                      round(df["RSI"].mean(), 1),
    }


def kpi_card_table(kpis: dict) -> pd.DataFrame:
    rows = [
        ("Engagement Retention Ratio",   f"{kpis['engagement_retention_ratio']}×",
         "Inactive customers churn this many times more than active ones"),
        ("Active Member Churn Rate",     f"{kpis['active_churn_pct']}%",
         "Churn rate among IsActiveMember = 1"),
        ("Inactive Member Churn Rate",   f"{kpis['inactive_churn_pct']}%",
         "Churn rate among IsActiveMember = 0"),
        ("Product Depth Index",          f"{kpis['product_depth_index']}",
         "Avg products (retained) / Avg products (churned)"),
        ("Credit Card Stickiness Score", f"{kpis['credit_card_stickiness_score']} pp",
         "Churn reduction (pp) for credit card holders vs non-holders"),
        ("High-Balance Disengagement %", f"{kpis['high_balance_inactive_pct']}%",
         "% of top-quartile balance customers who are inactive"),
        ("High-Balance Churn Rate",      f"{kpis['high_balance_churn_pct']}%",
         "Churn rate in the premium balance segment"),
        ("Sticky Customer Churn Rate",   f"{kpis['sticky_churn_pct']}%",
         "Churn among active + 2 products + credit card + 3yr+ tenure"),
        ("Non-Sticky Churn Rate",        f"{kpis['non_sticky_churn_pct']}%",
         "Churn among customers not meeting sticky criteria"),
        ("Retention Advantage (Sticky)", f"{kpis['sticky_retention_advantage']} pp",
         "Percentage-point improvement of sticky over non-sticky"),
        ("Avg Relationship Strength",    f"{kpis['avg_rsi']} / 100",
         "Mean RSI score across all customers"),
    ]
    return pd.DataFrame(rows, columns=["KPI", "Value", "Description"])
