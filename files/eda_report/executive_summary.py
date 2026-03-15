"""
executive_summary.py
Run from project root: python executive_summary.py
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from data_loader        import load_data, dataset_summary
from engagement         import classify_engagement, engagement_retention_ratio, gender_churn_summary
from product_analysis   import single_vs_multi_retention, credit_card_stickiness, geography_churn_summary
from financial_analysis import high_balance_disengagement_rate, identify_at_risk_premium
from retention          import define_sticky_customers, sticky_vs_non_sticky_churn, relationship_strength_index
from kpi                import compute_all_kpis


def generate():
    df = load_data("bank_churn.csv")
    df = classify_engagement(df)
    df = relationship_strength_index(df)
    df = define_sticky_customers(df)

    s    = dataset_summary(df)
    kpis = compute_all_kpis(df)
    err  = engagement_retention_ratio(df)
    smr  = single_vs_multi_retention(df)
    ccs  = credit_card_stickiness(df)
    hbdr = high_balance_disengagement_rate(df)
    svns = sticky_vs_non_sticky_churn(df)
    ar   = identify_at_risk_premium(df)
    geo  = geography_churn_summary(df)
    gen  = gender_churn_summary(df)

    lines = []
    def w(s=""): lines.append(str(s))

    w("╔" + "═"*76 + "╗")
    w("║                       EXECUTIVE SUMMARY                                   ║")
    w("║  Customer Engagement & Product Utilization Analytics for Retention         ║")
    w("║  European Bank Dataset (Year 2025, N = 10,000)                            ║")
    w("║  Prepared for: European Central Bank & Government Stakeholders             ║")
    w("╚" + "═"*76 + "╝")
    w()
    w("PURPOSE"); w("─"*78)
    w("Data-driven analysis of customer churn at a European bank. 10,000 customers")
    w("across France, Spain, and Germany. Focus: behavioural engagement and product")
    w("usage — not demographics — as the primary drivers of retention.")
    w()
    w("SCALE OF THE CHALLENGE"); w("─"*78)
    w(f"  • {s['churn_count']:,} customers ({s['churn_rate']}%) churned — nearly 1 in 5.")
    w(f"  • {s['inactive_members']:,} customers ({s['inactive_members']/s['total_customers']*100:.1f}%) are currently inactive.")
    w(f"  • {s['zero_balance']:,} customers ({s['zero_balance']/s['total_customers']*100:.1f}%) hold zero balance.")
    w(f"  • {len(ar):,} premium customers are disengaged — highest silent churn risk.")
    w()
    w("KEY FINDINGS"); w("─"*78)
    w()
    w(f"  1. ENGAGEMENT RETENTION RATIO: {kpis['engagement_retention_ratio']}×")
    w(f"     Active churn: {err['active_churn_rate']}%  |  Inactive churn: {err['inactive_churn_rate']}%")
    w()
    w(f"  2. THE 3-PRODUCT CLIFF")
    w(f"     2-product churn: {smr['two_product_churn']}% (optimal)  |  3+: {smr['three_plus_product_churn']}% (critical failure)")
    w()
    w(f"  3. GERMANY REGIONAL RISK")
    for _, row in geo.iterrows():
        w(f"     {row['Geography']}: {row['ChurnRate']}%")
    w()
    w(f"  4. GENDER CHURN GAP")
    for _, row in gen.iterrows():
        w(f"     {row['Gender']}: {row['ChurnRate']}%")
    w()
    w(f"  5. CREDIT CARD STICKINESS: {kpis['credit_card_stickiness_score']} pp")
    w(f"     Card holders: {ccs['card_holder_churn']}%  |  No card: {ccs['no_card_churn']}%")
    w()
    w(f"  6. HIGH-BALANCE DISENGAGEMENT: {kpis['high_balance_inactive_pct']}%")
    w(f"     {hbdr['inactive_pct']}% of premium customers inactive. Balance ≠ loyalty.")
    w()
    w(f"  7. STICKY RETENTION ADVANTAGE: {kpis['sticky_retention_advantage']} pp")
    w(f"     Sticky: {svns['sticky_churn_rate']}%  |  Non-Sticky: {svns['non_sticky_churn_rate']}%")
    w()
    w("STRATEGIC RECOMMENDATIONS"); w("─"*78)
    w()
    w(f"  P1 — INACTIVE RE-ENGAGEMENT [IMMEDIATE]")
    w(f"       Target {s['inactive_members']:,} inactive members. Trigger: 90+ day inactivity.")
    w()
    w(f"  P2 — 3-PRODUCT BUNDLE AUDIT [URGENT]")
    w(f"       3+ products = {smr['three_plus_product_churn']}% churn. Audit and redesign all bundles.")
    w()
    w(f"  P3 — PREMIUM SILENT CHURN PROGRAMME [HIGH VALUE]")
    w(f"       Assign relationship managers to {len(ar):,} at-risk premium customers.")
    w()
    w(f"  P4 — GERMANY REGIONAL PROGRAMME [STRATEGIC]")
    w(f"       Germany at 32.44% churn. Local product audit + dedicated support.")
    w()
    w(f"  P5 — GENDER-RESPONSIVE ENGAGEMENT [SCALABLE]")
    w(f"       Female churn 25.07% vs male 16.46%. Targeted campaigns needed.")
    w()
    w(f"  P6 — CREDIT CARD ACQUISITION PUSH [LONG-TERM]")
    w(f"       Only {s['has_credit_card']/s['total_customers']*100:.0f}% hold a card. Offer first-year fee waivers.")
    w()
    w(f"  P7 — RSI CRM INTEGRATION [SYSTEMIC]")
    w(f"       Flag RSI < 30 for monthly automated outreach.")
    w()
    w("CONCLUSION"); w("─"*78)
    w("Engagement and product alignment — not balance — drive retention.")
    w("Three priorities demand immediate action: inactivity gap, 3-product cliff,")
    w("and Germany regional risk. The KPI framework is ready for CRM integration.")
    w()
    w("─"*78)
    w("European_Bank.csv | Year 2025 | Unified Mentor — European Central Bank")
    w("─"*78)

    text = "\n".join(lines)
    with open("executive_summary.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(text)
    print("\n✅  Saved: executive_summary.txt")


if __name__ == "__main__":
    generate()
