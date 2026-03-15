"""
pages/02_Product_Utilization.py
Module 2: Product Utilization Impact Analysis
Key insight: 3-product cliff — 82.71% churn at 3 products, 100% at 4.
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import plotly.graph_objects as go
from data_loader      import load_data
from engagement       import classify_engagement
from product_analysis import (product_churn_summary, single_vs_multi_retention,
                               product_depth_index, credit_card_stickiness,
                               product_mix_by_geography, product_churn_heatmap_data,
                               geography_churn_summary)
from visualizations   import (bar_product_churn, heatmap_product_activity,
                               bar_geography_products, bar_geography_churn)

st.set_page_config(page_title="Product Utilization", page_icon="📦", layout="wide")

@st.cache_data
def get_data():
    df = load_data("bank_churn.csv")
    return classify_engagement(df)

df_raw = get_data()

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.header("🔧 Filters")
geo_options  = ["All"] + sorted(df_raw["Geography"].unique().tolist())
selected_geo = st.sidebar.selectbox("Geography", geo_options)
prod_range   = st.sidebar.slider("Number of Products", 1, 4, (1, 4))
selected_gen = st.sidebar.radio("Gender", ["All", "Male", "Female"])

df = df_raw.copy()
if selected_geo != "All": df = df[df["Geography"] == selected_geo]
if selected_gen != "All": df = df[df["Gender"]    == selected_gen]
df = df[(df["NumOfProducts"] >= prod_range[0]) & (df["NumOfProducts"] <= prod_range[1])]

# ── Page ──────────────────────────────────────────────────────────────────────
st.title("📦 Product Utilization Impact Analysis")
st.markdown("⚠️ Real data reveals a **3-product cliff** — churn spikes to **82.71%** at 3 products and **100%** at 4.")
st.divider()

smr = single_vs_multi_retention(df)
pdi = product_depth_index(df)
ccs = credit_card_stickiness(df)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("1-Product Churn",    f"{smr['single_product_churn']}%")
c2.metric("2-Product Churn",    f"{smr['two_product_churn']}%",
          delta=f"{smr['retention_lift_1_to_2']:+.1f} pp vs single")
c3.metric("3+ Product Churn",   f"{smr['three_plus_product_churn']}%",
          delta_color="inverse")
c4.metric("Product Depth Index",f"{pdi}")
c5.metric("CC Stickiness",      f"{ccs['stickiness_score']} pp")
st.divider()

st.subheader("📊 Churn Rate by Number of Products")
c1, c2 = st.columns([3, 2])
with c1:
    st.plotly_chart(bar_product_churn(product_churn_summary(df)), use_container_width=True)
with c2:
    st.markdown("#### Product Depth Summary")
    st.dataframe(
        product_churn_summary(df)
        .style.format({"ChurnRate": "{:.2f}%", "RetentionRate": "{:.2f}%"}),
        use_container_width=True, hide_index=True
    )
    st.info(
        f"**2-product customers** churn at only **{smr['two_product_churn']}%** — "
        f"the optimal count. 3+ products show extreme churn, likely from misaligned bundles."
    )
st.divider()

st.subheader("🔥 Churn Heatmap: Products × Activity Status")
pivot = product_churn_heatmap_data(df)
st.plotly_chart(heatmap_product_activity(pivot), use_container_width=True)
st.divider()

st.subheader("🌍 Geography Analysis")
c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(bar_geography_churn(geography_churn_summary(df)), use_container_width=True)
with c2:
    st.plotly_chart(bar_geography_products(product_mix_by_geography(df)), use_container_width=True)
st.divider()

st.subheader("💳 Credit Card Stickiness Score")
c1, c2 = st.columns(2)
with c1:
    st.info(
        f"**Card Holders ({ccs['card_holder_count']:,}):** {ccs['card_holder_churn']}% churn  \n"
        f"**No Credit Card ({ccs['no_card_count']:,}):** {ccs['no_card_churn']}% churn  \n"
        f"**Stickiness Advantage:** {ccs['stickiness_score']} percentage points"
    )
with c2:
    fig = go.Figure(go.Bar(
        x=["Card Holders", "No Credit Card"],
        y=[ccs["card_holder_churn"], ccs["no_card_churn"]],
        marker_color=["#1A73E8", "#EA4335"],
        text=[f"{ccs['card_holder_churn']}%", f"{ccs['no_card_churn']}%"],
        textposition="outside",
    ))
    fig.update_layout(yaxis_title="Churn Rate (%)", height=300,
                      template="plotly_white",
                      margin=dict(l=20, r=20, t=30, b=20),
                      paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
