"""
pages/01_Engagement_Overview.py
Module 1: Engagement vs Churn Overview
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_loader     import load_data, dataset_summary
from engagement      import (classify_engagement, engagement_retention_ratio,
                              profile_churn_summary, tenure_churn_summary,
                              gender_churn_summary, age_group_churn)
from visualizations  import (bar_profile_churn, pie_engagement_distribution,
                              line_tenure_churn, gauge_chart,
                              bar_gender_churn, bar_age_group_churn)

st.set_page_config(page_title="Engagement Overview", page_icon="📊", layout="wide")

@st.cache_data
def get_data():
    df = load_data("bank_churn.csv")
    return classify_engagement(df)

df_raw = get_data()

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.header("🔧 Filters")
geo_options      = ["All"] + sorted(df_raw["Geography"].unique().tolist())
selected_geo     = st.sidebar.selectbox("Geography", geo_options)
selected_gender  = st.sidebar.radio("Gender", ["All", "Male", "Female"])
selected_activity= st.sidebar.radio("Activity Status", ["All", "Active (1)", "Inactive (0)"])
min_t, max_t     = int(df_raw["Tenure"].min()), int(df_raw["Tenure"].max())
tenure_range     = st.sidebar.slider("Tenure Range (years)", min_t, max_t, (min_t, max_t))

df = df_raw.copy()
if selected_geo      != "All":       df = df[df["Geography"]      == selected_geo]
if selected_gender   != "All":       df = df[df["Gender"]         == selected_gender]
if selected_activity == "Active (1)":  df = df[df["IsActiveMember"] == 1]
elif selected_activity == "Inactive (0)": df = df[df["IsActiveMember"] == 0]
df = df[(df["Tenure"] >= tenure_range[0]) & (df["Tenure"] <= tenure_range[1])]

# ── Page ──────────────────────────────────────────────────────────────────────
st.title("📊 Engagement vs Churn Overview")
st.markdown("Explore how **engagement**, **gender**, and **age** drive churn. Use the sidebar to filter.")
st.divider()

summary = dataset_summary(df)
err     = engagement_retention_ratio(df)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("👥 Customers",         f"{summary['total_customers']:,}")
c2.metric("⚠️ Churned",           f"{summary['churn_count']:,}",
          f"{summary['churn_rate']}%", delta_color="inverse")
c3.metric("✅ Active Members",     f"{summary['active_members']:,}")
c4.metric("😴 Inactive Members",  f"{summary['inactive_members']:,}")
c5.metric("📦 Avg Products",      summary['avg_products'])
st.divider()

st.subheader("🎯 Engagement Retention Ratio (ERR)")
st.markdown(
    f"Inactive members churn **{err['ratio']}× more** than active members.  "
    f"Active: **{err['active_churn_rate']}%** | Inactive: **{err['inactive_churn_rate']}%**"
)
g1, g2, g3 = st.columns(3)
with g1:
    st.plotly_chart(gauge_chart(err["active_churn_rate"],   "Active Churn %",   low=15, high=30), use_container_width=True)
with g2:
    st.plotly_chart(gauge_chart(err["inactive_churn_rate"], "Inactive Churn %", low=25, high=45), use_container_width=True)
with g3:
    st.plotly_chart(gauge_chart(min(err["ratio"] * 20, 100), "ERR Score (×20 scaled)", low=30, high=60), use_container_width=True)
st.divider()

st.subheader("📋 Engagement Profile Analysis")
c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(bar_profile_churn(profile_churn_summary(df)), use_container_width=True)
with c2:
    st.plotly_chart(pie_engagement_distribution(df), use_container_width=True)
st.divider()

st.subheader("👤 Churn by Gender & Age Group")
c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(bar_gender_churn(gender_churn_summary(df)), use_container_width=True)
with c2:
    st.plotly_chart(bar_age_group_churn(age_group_churn(df)), use_container_width=True)
st.divider()

st.subheader("📅 Churn Rate by Tenure")
st.plotly_chart(line_tenure_churn(tenure_churn_summary(df)), use_container_width=True)
st.divider()

st.subheader("📄 Profile Summary Table")
st.dataframe(
    profile_churn_summary(df).style.format({"ChurnRate": "{:.2f}%"}),
    use_container_width=True, hide_index=True
)
