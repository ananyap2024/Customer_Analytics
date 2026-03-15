"""
pages/04_Retention_Scoring.py
Module 4: Retention Strength Scoring Panels
RSI tiers, sticky customer profiles, thresholds, full KPI table.
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import plotly.express as px
from data_loader    import load_data
from engagement     import classify_engagement
from retention      import (define_sticky_customers, sticky_vs_non_sticky_churn,
                             engagement_tier_stability, rsi_churn_summary,
                             relationship_strength_index, engagement_threshold_analysis)
from kpi            import compute_all_kpis, kpi_card_table
from visualizations import (bar_rsi_churn, bar_tier_retention,
                             line_threshold_churn, gauge_chart)

st.set_page_config(page_title="Retention Scoring", page_icon="🏆", layout="wide")

@st.cache_data
def get_data():
    df = load_data("bank_churn.csv")
    df = classify_engagement(df)
    df = relationship_strength_index(df)
    df = define_sticky_customers(df)
    return df

df_raw = get_data()

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.header("🔧 Filters")
geo_options  = ["All"] + sorted(df_raw["Geography"].unique().tolist())
selected_geo = st.sidebar.selectbox("Geography", geo_options)
selected_gen = st.sidebar.radio("Gender", ["All", "Male", "Female"])
min_rsi      = st.sidebar.slider("Minimum RSI Score", 0, 100, 0)

df = df_raw.copy()
if selected_geo != "All": df = df[df["Geography"] == selected_geo]
if selected_gen != "All": df = df[df["Gender"]    == selected_gen]
df = df[df["RSI"] >= min_rsi]

# ── Page ──────────────────────────────────────────────────────────────────────
st.title("🏆 Retention Strength Scoring")
st.markdown("RSI tiers, sticky profiles, engagement thresholds, and the complete KPI dashboard.")
st.divider()

kpis   = compute_all_kpis(df)
kpi_df = kpi_card_table(kpis)
st.subheader("📌 Complete KPI Dashboard")
st.dataframe(kpi_df.style.set_properties(**{"text-align": "left"}),
             use_container_width=True, hide_index=True)
st.divider()

st.subheader("🔵 Relationship Strength Index (RSI) Tiers")
st.markdown(
    "RSI = **IsActiveMember** (30 pts) + **HasCrCard** (15 pts) + "
    "**2 Products** (20 pts) + **Tenure** (up to 15 pts).  "
    "3+ products receive 0 pts due to the churn cliff."
)
c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(bar_rsi_churn(rsi_churn_summary(df)), use_container_width=True)
with c2:
    st.plotly_chart(bar_tier_retention(engagement_tier_stability(df)), use_container_width=True)
st.divider()

st.subheader("🔒 Sticky Customer Profile")
st.markdown("**Sticky:** Active + exactly 2 products + Credit card + ≥3 years tenure")
svns = sticky_vs_non_sticky_churn(df)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Sticky Customers",     f"{svns['sticky_count']:,}")
c2.metric("Non-Sticky",           f"{svns['non_sticky_count']:,}")
c3.metric("Sticky Churn",         f"{svns['sticky_churn_rate']}%")
c4.metric("Non-Sticky Churn",     f"{svns['non_sticky_churn_rate']}%",
          delta=f"+{svns['retention_advantage']} pp", delta_color="inverse")
st.success(
    f"✅ Sticky customers churn at **{svns['sticky_churn_rate']}%** vs "
    f"**{svns['non_sticky_churn_rate']}%** for non-sticky — "
    f"a **{svns['retention_advantage']} pp advantage**."
)

sticky_df = df[df["IsSticky"] == 1][
    ["CustomerId","Geography","Gender","Age","Tenure","Balance",
     "NumOfProducts","CreditScore","RSI","RSI_Tier","Exited"]
].sort_values("RSI", ascending=False).head(50)
with st.expander("👁️ View Top 50 Sticky Customers"):
    st.dataframe(
        sticky_df.style.format({"Balance": "€{:,.2f}"}),
        use_container_width=True, hide_index=True
    )
st.divider()

st.subheader("📊 RSI Score Distribution by Tier")
fig_hist = px.histogram(
    df, x="RSI", color="RSI_Tier", nbins=20, barmode="overlay",
    color_discrete_sequence=["#EA4335","#FBBC04","#1A73E8","#34A853"],
    labels={"RSI": "Relationship Strength Index Score"}, opacity=0.75,
)
fig_hist.update_layout(template="plotly_white", height=350,
                       paper_bgcolor="rgba(0,0,0,0)",
                       margin=dict(l=30,r=20,t=40,b=30))
st.plotly_chart(fig_hist, use_container_width=True)
st.divider()

st.subheader("📉 Engagement Score Threshold vs Churn Rate")
st.markdown("Find the score above which churn drops significantly — the minimum engagement needed for effective retention.")
thresh_df = engagement_threshold_analysis(df)
st.plotly_chart(line_threshold_churn(thresh_df), use_container_width=True)
with st.expander("📄 Threshold Data Table"):
    st.dataframe(
        thresh_df.dropna().style.format({"Above_ChurnRate":"{:.2f}%","Below_ChurnRate":"{:.2f}%"}),
        use_container_width=True, hide_index=True
    )
