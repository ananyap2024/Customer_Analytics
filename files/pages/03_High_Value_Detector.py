"""
pages/03_High_Value_Detector.py
Module 3: High-Value Disengaged Customer Detector
621 at-risk premium customers identified with export capability.
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import plotly.express as px
from data_loader        import load_data
from engagement         import classify_engagement
from financial_analysis import (
    balance_activity_churn_matrix, mismatch_churn_summary,
    identify_at_risk_premium, high_balance_disengagement_rate,
    balance_churn_by_geography, credit_score_segment_churn,
)
from visualizations import (
    bar_balance_activity_churn, scatter_balance_salary,
    bar_balance_geography, bar_credit_score_churn,
)

st.set_page_config(page_title="High-Value Detector", page_icon="🔍", layout="wide")

@st.cache_data
def get_data():
    df = load_data("bank_churn.csv")
    return classify_engagement(df)

df_raw = get_data()

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.header("🔧 Filters")
balance_pct  = st.sidebar.slider("High-Balance Percentile Threshold", 50, 95, 75)
salary_pct   = st.sidebar.slider("High-Salary Percentile Threshold",  25, 75, 50)
geo_options  = ["All"] + sorted(df_raw["Geography"].unique().tolist())
selected_geo = st.sidebar.selectbox("Geography", geo_options)
selected_gen = st.sidebar.radio("Gender", ["All", "Male", "Female"])

df = df_raw.copy()
if selected_geo != "All": df = df[df["Geography"] == selected_geo]
if selected_gen != "All": df = df[df["Gender"]    == selected_gen]

# ── Page ──────────────────────────────────────────────────────────────────────
st.title("🔍 High-Value Disengaged Customer Detector")
st.markdown("Identify **premium customers** who are financially committed but behaviourally disengaged — highest **silent churn** risk.")
st.divider()

hbdr       = high_balance_disengagement_rate(df)
at_risk_df = identify_at_risk_premium(df, balance_pct / 100, salary_pct / 100)

c1, c2, c3, c4 = st.columns(4)
c1.metric("High-Balance Threshold",  f"€{hbdr['high_balance_threshold']:,.0f}")
c2.metric("High-Balance Customers",  f"{hbdr['high_balance_count']:,}")
c3.metric("Inactive Among Premium",  f"{hbdr['inactive_pct']}%")
c4.metric("Premium Churn Rate",      f"{hbdr['churn_rate']}%",
          delta=f"+{hbdr['churn_rate']:.1f}%", delta_color="inverse")
st.divider()

st.subheader(f"⚠️ At-Risk Premium Customers — {len(at_risk_df):,} Identified")
st.markdown(
    f"Balance ≥ **{balance_pct}th percentile** (€{df['Balance'].quantile(balance_pct/100):,.0f})  AND  "
    f"Salary ≥ **{salary_pct}th percentile** (€{df['EstimatedSalary'].quantile(salary_pct/100):,.0f})  AND  "
    f"**Inactive member**."
)

display_cols = ["CustomerId", "Geography", "Gender", "Age", "Tenure",
                "Balance", "EstimatedSalary", "NumOfProducts",
                "HasCrCard", "CreditScore", "EngagementProfile", "Exited"]

if len(at_risk_df) > 0:
    churn_pct = at_risk_df["Exited"].mean() * 100
    st.warning(f"🚨 **{churn_pct:.1f}%** of these at-risk premium customers have already churned.")
    st.dataframe(
        at_risk_df[display_cols].sort_values("Balance", ascending=False).head(100)
        .style
        .format({"Balance": "€{:,.2f}", "EstimatedSalary": "€{:,.2f}"})
        .applymap(lambda v: "background-color:#FADBD8" if v == 1 else "", subset=["Exited"]),
        use_container_width=True, hide_index=True
    )
    st.download_button(
        "⬇️ Download At-Risk Customer List (CSV)",
        data=at_risk_df[display_cols].to_csv(index=False),
        file_name="at_risk_premium_customers.csv", mime="text/csv"
    )
else:
    st.info("No at-risk customers match the current filter criteria.")
st.divider()

st.subheader("📊 Balance Segment × Activity — Churn Matrix")
c1, c2 = st.columns([3, 2])
with c1:
    st.plotly_chart(bar_balance_activity_churn(balance_activity_churn_matrix(df)), use_container_width=True)
with c2:
    matrix = balance_activity_churn_matrix(df)
    st.dataframe(
        matrix[["BalanceSegment","Activity","Total","Churned","ChurnRate"]]
        .style.format({"ChurnRate": "{:.2f}%"}),
        use_container_width=True, hide_index=True
    )
st.divider()

st.subheader("💰 Balance vs Salary Distribution — Churn Overlay")
st.plotly_chart(scatter_balance_salary(df), use_container_width=True)
st.divider()

st.subheader("🚨 Salary–Balance Mismatch Analysis")
mismatch_tbl = mismatch_churn_summary(df)
c1, c2 = st.columns(2)
with c1:
    st.dataframe(
        mismatch_tbl.style.format({"ChurnRate": "{:.2f}%"}),
        use_container_width=True, hide_index=True
    )
with c2:
    fig = px.bar(mismatch_tbl, x="MismatchRisk", y="ChurnRate",
                 color="MismatchRisk", color_discrete_sequence=["#EA4335","#1A73E8"],
                 text="ChurnRate")
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(template="plotly_white", height=300, showlegend=False,
                      paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=20,r=20,t=30,b=20))
    st.plotly_chart(fig, use_container_width=True)
st.divider()

st.subheader("📈 Churn Rate by Credit Score Band  (Range: 350–850)")
st.plotly_chart(bar_credit_score_churn(credit_score_segment_churn(df)), use_container_width=True)
st.divider()

st.subheader("🌍 Average Balance by Geography & Churn Status")
st.plotly_chart(bar_balance_geography(balance_churn_by_geography(df)), use_container_width=True)
