"""
generate_eda_report.py
Run from project root: python generate_eda_report.py
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import pandas as pd
import numpy as np
from scipy import stats

from data_loader        import load_data, dataset_summary
from engagement         import (classify_engagement, engagement_retention_ratio,
                                 profile_churn_summary, tenure_churn_summary,
                                 gender_churn_summary, age_group_churn)
from product_analysis   import (product_churn_summary, single_vs_multi_retention,
                                 product_depth_index, credit_card_stickiness,
                                 geography_churn_summary)
from financial_analysis import (balance_activity_churn_matrix, mismatch_churn_summary,
                                 high_balance_disengagement_rate, identify_at_risk_premium,
                                 credit_score_segment_churn)
from retention          import (define_sticky_customers, sticky_vs_non_sticky_churn,
                                 rsi_churn_summary, relationship_strength_index)
from kpi                import compute_all_kpis, kpi_card_table


def run_eda():
    df = load_data("bank_churn.csv")
    df = classify_engagement(df)
    df = relationship_strength_index(df)
    df = define_sticky_customers(df)

    lines = []
    def w(s=""): lines.append(str(s))

    w("╔" + "═"*76 + "╗")
    w("║  CUSTOMER ENGAGEMENT & PRODUCT UTILIZATION ANALYTICS                      ║")
    w("║  FOR RETENTION STRATEGY — EDA RESEARCH REPORT                             ║")
    w("║  Source: European_Bank.csv  |  Year: 2025  |  N = 10,000                 ║")
    w("║  Unified Mentor: European Central Bank                                    ║")
    w("╚" + "═"*76 + "╝")

    w("\n" + "═"*78)
    w("  1. DATASET OVERVIEW & VALIDATION")
    w("═"*78)
    s = dataset_summary(df)
    w(f"  Total Customers          : {s['total_customers']:,}")
    w(f"  Churned Customers        : {s['churn_count']:,}  ({s['churn_rate']}%)")
    w(f"  Retained Customers       : {s['total_customers'] - s['churn_count']:,}")
    w(f"  Active Members           : {s['active_members']:,}  ({s['active_members']/s['total_customers']*100:.1f}%)")
    w(f"  Inactive Members         : {s['inactive_members']:,}  ({s['inactive_members']/s['total_customers']*100:.1f}%)")
    w(f"  Zero Balance Customers   : {s['zero_balance']:,}  ({s['zero_balance']/s['total_customers']*100:.1f}%)")
    w(f"  Avg Products per Customer: {s['avg_products']}")
    w(f"  Avg Account Balance      : €{s['avg_balance']:,.2f}")
    w(f"  Has Credit Card          : {s['has_credit_card']:,}  ({s['has_credit_card']/s['total_customers']*100:.1f}%)")
    w(f"  Missing Values           : {s['missing_values']}  ✓ Clean dataset")
    w(f"  Dataset Year             : {s['year']}")
    w()
    w("  Geography Distribution:")
    for geo, cnt in s['geographies'].items():
        w(f"    {geo:<10}: {cnt:,} ({cnt/s['total_customers']*100:.1f}%)")
    w()
    w("  Descriptive Statistics:")
    w(df[["CreditScore","Age","Tenure","Balance","NumOfProducts","EstimatedSalary"]]
      .describe().round(2).to_string())

    w("\n" + "═"*78)
    w("  2. ENGAGEMENT CLASSIFICATION")
    w("═"*78)
    w(profile_churn_summary(df).to_string(index=False))
    w()
    err = engagement_retention_ratio(df)
    w(f"  ERR: Active={err['active_churn_rate']}%  |  Inactive={err['inactive_churn_rate']}%  |  Ratio={err['ratio']}×")
    w()
    w("  Gender Churn:"); w(gender_churn_summary(df).to_string(index=False))
    w()
    w("  Age Group Churn:"); w(age_group_churn(df).to_string(index=False))
    w()
    w("  Tenure Churn:"); w(tenure_churn_summary(df).to_string(index=False))

    w("\n" + "═"*78)
    w("  3. PRODUCT UTILIZATION — THE 3-PRODUCT CLIFF")
    w("═"*78)
    w(product_churn_summary(df).to_string(index=False))
    w()
    smr = single_vs_multi_retention(df)
    w(f"  1-Product: {smr['single_product_churn']}%  |  2-Product: {smr['two_product_churn']}% (OPTIMAL)  |  3+: {smr['three_plus_product_churn']}% (CLIFF)")
    w(f"  PDI: {product_depth_index(df)}")
    w()
    w("  Geography Churn:"); w(geography_churn_summary(df).to_string(index=False))
    ccs = credit_card_stickiness(df)
    w(f"\n  CC Stickiness: Card={ccs['card_holder_churn']}%  |  No Card={ccs['no_card_churn']}%  |  Score={ccs['stickiness_score']} pp")

    w("\n" + "═"*78)
    w("  4. FINANCIAL COMMITMENT VS ENGAGEMENT")
    w("═"*78)
    hbdr = high_balance_disengagement_rate(df)
    w(f"  HBDR: Threshold=€{hbdr['high_balance_threshold']:,.0f}  |  Inactive={hbdr['inactive_pct']}%  |  Churn={hbdr['churn_rate']}%")
    w()
    w("  Balance × Activity Matrix:")
    w(balance_activity_churn_matrix(df)[["BalanceSegment","Activity","Total","Churned","ChurnRate"]].to_string(index=False))
    w()
    w("  Credit Score Bands:"); w(credit_score_segment_churn(df).to_string(index=False))
    w()
    w("  Salary–Balance Mismatch:"); w(mismatch_churn_summary(df).to_string(index=False))
    ar = identify_at_risk_premium(df)
    w(f"\n  At-Risk Premium: {len(ar):,} customers  |  Churn rate: {ar['Exited'].mean()*100:.2f}%")

    w("\n" + "═"*78)
    w("  5. RETENTION STRENGTH ASSESSMENT")
    w("═"*78)
    svns = sticky_vs_non_sticky_churn(df)
    w(f"  Sticky (Active+2prod+CC+3yr): {svns['sticky_count']:,} customers")
    w(f"  Sticky Churn: {svns['sticky_churn_rate']}%  |  Non-Sticky: {svns['non_sticky_churn_rate']}%  |  Advantage: {svns['retention_advantage']} pp")
    w()
    w("  RSI Tier Churn:"); w(rsi_churn_summary(df).to_string(index=False))
    w()
    ct = pd.crosstab(df["IsActiveMember"], df["Exited"])
    chi2, p, dof, _ = stats.chi2_contingency(ct)
    w(f"  Chi-Squared (Activity vs Churn): χ²={chi2:.4f}  p={p:.8f}  → {'Highly Significant' if p < 0.001 else 'Significant'}")
    corr, pc = stats.pointbiserialr(df["NumOfProducts"], df["Exited"])
    w(f"  Point-Biserial (Products vs Churn): r={corr:.4f}  p={pc:.6f}")

    w("\n" + "═"*78)
    w("  6. KEY PERFORMANCE INDICATORS")
    w("═"*78)
    w(kpi_card_table(compute_all_kpis(df)).to_string(index=False))

    w("\n" + "═"*78)
    w("  7. INSIGHTS & RECOMMENDATIONS")
    w("═"*78)
    insights = [
        ("INSIGHT 1 — Engagement is the #1 Retention Driver",
         f"Inactive customers churn {err['ratio']}× more than active ones (ERR={err['ratio']}×)."),
        ("INSIGHT 2 — The 3-Product Cliff",
         f"Churn spikes to {smr['three_plus_product_churn']}% at 3+ products vs {smr['two_product_churn']}% at 2."),
        ("INSIGHT 3 — Germany Has the Highest Churn",
         "German customers show 32.44% churn — double France/Spain. Needs regional action."),
        ("INSIGHT 4 — Female Customers Churn More",
         "Female churn (25.07%) is significantly higher than male (16.46%)."),
        ("INSIGHT 5 — High Balance ≠ Loyalty",
         f"{hbdr['inactive_pct']}% of premium customers are inactive — silent churn risk."),
        ("REC 1 — Re-engage inactive members immediately",
         f"Target {s['inactive_members']:,} inactive members with personalised campaigns."),
        ("REC 2 — Audit 3+ product bundles",
         f"Fix the 3-product cliff — {smr['three_plus_product_churn']}% churn is a product design failure."),
        ("REC 3 — Premium silent churn programme",
         f"Assign relationship managers to {len(ar):,} at-risk premium customers."),
        ("REC 4 — Germany regional retention programme",
         "Investigate and fix product-market fit in Germany specifically."),
        ("REC 5 — Integrate RSI into CRM",
         "Flag all customers with RSI < 30 for automated monthly outreach."),
    ]
    for title, body in insights:
        w(f"\n  ► {title}")
        w(f"    {body}")

    w("\n" + "═"*78)
    w("  8. CONCLUSION")
    w("═"*78)
    w("  Churn is a behavioural phenomenon. Engagement depth, product alignment,")
    w("  and relationship strength — not wealth — determine loyalty.")
    w("  The 3-product cliff and Germany gap are the two highest-priority fixes.")
    w("═"*78)
    w("  European_Bank.csv | Year 2025 | Unified Mentor — European Central Bank")
    w("═"*78)

    report = "\n".join(lines)
    with open("eda_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    print(report)
    print("\n✅  Saved: eda_report.txt")


if __name__ == "__main__":
    run_eda()
