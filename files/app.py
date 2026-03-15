"""
app.py  –  Main Streamlit Home Page
Customer Engagement & Product Utilization Analytics for Retention Strategy
European Bank Dataset | Year: 2025 | 10,000 customers
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import plotly.express as px
from data_loader import load_data, dataset_summary
from engagement import classify_engagement
from retention import relationship_strength_index, define_sticky_customers
from kpi import compute_all_kpis

st.set_page_config(
    page_title="Customer Retention Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    [data-testid="stMetric"] {
        background-color: #F8F9FA;
        border: 1px solid #E0E7FF;
        border-radius: 10px;
        padding: 12px 16px;
    }
    [data-testid="stMetric"] label { font-weight: 600; color: #374151; }
    h1 { color: #1A3A5C; }
    h2, h3 { color: #2C3E50; }
    .block-container { padding-top: 1.5rem; }
    [data-testid="stSidebar"] { background-color: #EFF6FF; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def get_data():
    df = load_data("bank_churn.csv")
    df = classify_engagement(df)
    df = relationship_strength_index(df)
    df = define_sticky_customers(df)
    return df

df      = get_data()
summary = dataset_summary(df)
kpis    = compute_all_kpis(df)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🏦 Customer Engagement & Product Utilization Analytics")
st.markdown(
    f"**Unified Mentor Project** — European Central Bank  |  "
    f"**Dataset Year:** {summary['year']}  |  "
    f"**Source:** European Bank (10,000 customers)"
)
st.divider()

# ── Dataset Overview ──────────────────────────────────────────────────────────
st.subheader("📋 Dataset Overview")
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Total Customers",  f"{summary['total_customers']:,}")
c2.metric("Churned",          f"{summary['churn_count']:,}",
          delta=f"{summary['churn_rate']}%", delta_color="inverse")
c3.metric("Active Members",   f"{summary['active_members']:,}")
c4.metric("Avg Products",     summary['avg_products'])
c5.metric("Avg Balance",      f"€{summary['avg_balance']:,.0f}")
c6.metric("Zero Balance",     f"{summary['zero_balance']:,}",
          help="Customers with €0 balance")
st.divider()

# ── KPI Summary ───────────────────────────────────────────────────────────────
st.subheader("🎯 Key Performance Indicators at a Glance")
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Engagement Retention Ratio",  f"{kpis['engagement_retention_ratio']}×",
          help="Inactive customers churn this many times more than active ones")
k2.metric("Product Depth Index",         f"{kpis['product_depth_index']}",
          help="Avg products (retained) ÷ Avg products (churned)")
k3.metric("CC Stickiness Score",         f"{kpis['credit_card_stickiness_score']} pp",
          help="Churn reduction (pp) from credit card ownership")
k4.metric("High-Balance Disengaged",     f"{kpis['high_balance_inactive_pct']}%",
          help="% of premium-balance customers who are inactive")
k5.metric("Sticky Retention Advantage",  f"{kpis['sticky_retention_advantage']} pp",
          help="Churn gap: non-sticky vs sticky customers")
st.divider()

# ── Navigation ────────────────────────────────────────────────────────────────
st.subheader("🗺️ Navigate the Dashboard")
n1, n2, n3, n4 = st.columns(4)
with n1:
    st.info("### 📊 Engagement Overview\nEngagement profiles, activity-based "
            "churn, ERR, gender & age analysis.\n\n👈 *Sidebar → Page 1*")
with n2:
    st.info("### 📦 Product Utilization\n3-product cliff, heatmap, geography "
            "breakdown, CC stickiness.\n\n👈 *Sidebar → Page 2*")
with n3:
    st.warning("### 🔍 High-Value Detector\n621 premium disengaged customers "
               "identified. Export list.\n\n👈 *Sidebar → Page 3*")
with n4:
    st.success("### 🏆 Retention Scoring\nRSI tiers, sticky profiles, "
               "thresholds & full KPI table.\n\n👈 *Sidebar → Page 4*")
st.divider()

# ── Geography + Gender charts ─────────────────────────────────────────────────
st.subheader("🌍 Customer Distribution by Geography & Gender")
col_a, col_b = st.columns(2)

geo_df = df.groupby(["Geography", "Exited"]).size().reset_index(name="Count")
geo_df["Status"] = geo_df["Exited"].map({0: "Retained", 1: "Churned"})
with col_a:
    fig_geo = px.bar(geo_df, x="Geography", y="Count", color="Status",
                     barmode="stack", color_discrete_sequence=["#1A73E8", "#EA4335"],
                     text="Count")
    fig_geo.update_traces(textposition="inside")
    fig_geo.update_layout(template="plotly_white", height=350,
                          paper_bgcolor="rgba(0,0,0,0)",
                          margin=dict(l=30, r=20, t=40, b=30))
    st.plotly_chart(fig_geo, use_container_width=True)

gen_df = df.groupby(["Gender", "Exited"]).size().reset_index(name="Count")
gen_df["Status"] = gen_df["Exited"].map({0: "Retained", 1: "Churned"})
with col_b:
    fig_gen = px.bar(gen_df, x="Gender", y="Count", color="Status",
                     barmode="stack", color_discrete_sequence=["#1A73E8", "#EA4335"],
                     text="Count",
                     title="Customer Distribution by Gender & Churn Status")
    fig_gen.update_traces(textposition="inside")
    fig_gen.update_layout(template="plotly_white", height=350,
                          paper_bgcolor="rgba(0,0,0,0)",
                          margin=dict(l=30, r=20, t=40, b=30))
    st.plotly_chart(fig_gen, use_container_width=True)

st.divider()

# ── Data preview ──────────────────────────────────────────────────────────────
with st.expander("🔎 Preview Raw Dataset (first 50 rows)"):
    st.dataframe(
        df[["Year","CustomerId","Geography","Gender","Age","Tenure",
            "Balance","NumOfProducts","HasCrCard","IsActiveMember",
            "EstimatedSalary","CreditScore","Exited",
            "EngagementProfile","RSI","RSI_Tier"]]
        .head(50)
        .style.format({"Balance": "€{:,.2f}", "EstimatedSalary": "€{:,.2f}"})
        .applymap(lambda v: "background-color:#FADBD8" if v == 1 else "",
                  subset=["Exited"]),
        use_container_width=True, hide_index=True
    )

st.divider()
st.caption(
    "📌 Source: European_Bank.csv (10,000 customers, Year 2025) | "
    "Unified Mentor Initiative — European Central Bank | Built with Streamlit & Plotly"
)
