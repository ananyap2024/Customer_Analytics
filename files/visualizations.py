"""
visualizations.py
-----------------
16 reusable Plotly chart builders used across all Streamlit pages.
"""

import plotly.express       as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

PRIMARY   = "#1A73E8"
SECONDARY = "#EA4335"
ACCENT    = "#34A853"
WARN      = "#FBBC04"
NEUTRAL   = "#7F8C8D"
PALETTE   = [PRIMARY, SECONDARY, ACCENT, WARN, NEUTRAL, "#9B59B6", "#1ABC9C", "#E67E22"]


def _style(fig, title="", height=400):
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color="#2C3E50")),
        height=height, template="plotly_white",
        margin=dict(l=40, r=20, t=55, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="Inter, Arial", size=12),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def bar_profile_churn(df_summary):
    fig = px.bar(df_summary, x="EngagementProfile", y="ChurnRate",
                 color="EngagementProfile", color_discrete_sequence=PALETTE,
                 text="ChurnRate", labels={"ChurnRate": "Churn Rate (%)"})
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    return _style(fig, "Churn Rate by Engagement Profile")


def pie_engagement_distribution(df):
    counts = df["EngagementProfile"].value_counts().reset_index()
    counts.columns = ["Profile", "Count"]
    fig = px.pie(counts, names="Profile", values="Count",
                 color_discrete_sequence=PALETTE, hole=0.4)
    fig.update_traces(textinfo="percent+label")
    return _style(fig, "Engagement Profile Distribution")


def line_tenure_churn(df_tenure):
    fig = px.line(df_tenure, x="TenureBucket", y="ChurnRate",
                  markers=True, color_discrete_sequence=[PRIMARY],
                  labels={"ChurnRate": "Churn Rate (%)"})
    fig.update_traces(line_width=2.5, marker_size=8)
    return _style(fig, "Churn Rate by Customer Tenure")


def bar_gender_churn(df_gender):
    fig = px.bar(df_gender, x="Gender", y="ChurnRate",
                 color="Gender", color_discrete_sequence=[PRIMARY, SECONDARY],
                 text="ChurnRate", labels={"ChurnRate": "Churn Rate (%)"})
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    return _style(fig, "Churn Rate by Gender")


def bar_age_group_churn(df_age):
    fig = px.bar(df_age, x="AgeGroup", y="ChurnRate",
                 color="ChurnRate",
                 color_continuous_scale=["#2ECC71", "#F39C12", "#E74C3C"],
                 text="ChurnRate", labels={"ChurnRate": "Churn Rate (%)"})
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_coloraxes(showscale=False)
    return _style(fig, "Churn Rate by Age Group")


def bar_product_churn(df_product):
    fig = px.bar(df_product, x="NumOfProducts", y="ChurnRate",
                 color="ChurnRate",
                 color_continuous_scale=["#2ECC71", "#F39C12", "#E74C3C"],
                 text="ChurnRate",
                 labels={"ChurnRate": "Churn Rate (%)", "NumOfProducts": "# Products"})
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_coloraxes(showscale=False)
    return _style(fig, "Churn Rate by Number of Products")


def heatmap_product_activity(pivot):
    fig = go.Figure(go.Heatmap(
        z=pivot.values, x=pivot.columns.tolist(),
        y=[str(i) for i in pivot.index.tolist()],
        colorscale="RdYlGn_r", text=pivot.values,
        texttemplate="%{text:.1f}%", showscale=True,
        colorbar=dict(title="Churn %"),
    ))
    fig.update_layout(xaxis_title="Activity Status", yaxis_title="Number of Products")
    return _style(fig, "Churn Rate Heatmap: Products × Activity")


def bar_geography_products(df_geo):
    df_geo = df_geo.copy()
    df_geo["Status"] = df_geo["Churned"].map({0: "Retained", 1: "Churned"})
    fig = px.bar(df_geo, x="Geography", y="AvgProducts", color="Status",
                 barmode="group", color_discrete_sequence=[ACCENT, SECONDARY],
                 labels={"AvgProducts": "Avg # Products"})
    return _style(fig, "Avg Products by Geography & Churn Status")


def bar_geography_churn(df_geo):
    fig = px.bar(df_geo, x="Geography", y="ChurnRate",
                 color="Geography", color_discrete_sequence=PALETTE,
                 text="ChurnRate", labels={"ChurnRate": "Churn Rate (%)"})
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    return _style(fig, "Churn Rate by Geography")


def bar_balance_activity_churn(df_matrix):
    fig = px.bar(df_matrix, x="BalanceSegment", y="ChurnRate",
                 color="Activity", barmode="group",
                 color_discrete_sequence=[PRIMARY, SECONDARY],
                 labels={"ChurnRate": "Churn Rate (%)"})
    return _style(fig, "Churn Rate by Balance Segment & Activity")


def scatter_balance_salary(df, sample=2000):
    sample_df = df.sample(min(sample, len(df)), random_state=42).copy()
    sample_df["Status"] = sample_df["Exited"].map({0: "Retained", 1: "Churned"})
    fig = px.scatter(sample_df, x="EstimatedSalary", y="Balance",
                     color="Status", opacity=0.55,
                     color_discrete_sequence=[PRIMARY, SECONDARY],
                     labels={"EstimatedSalary": "Estimated Salary (€)", "Balance": "Account Balance (€)"})
    return _style(fig, "Balance vs Salary — Churn Distribution", height=450)


def bar_balance_geography(df_geo):
    df_geo = df_geo.copy()
    df_geo["Status"] = df_geo["Churned"].map({0: "Retained", 1: "Churned"})
    fig = px.bar(df_geo, x="Geography", y="AvgBalance", color="Status",
                 barmode="group", color_discrete_sequence=[ACCENT, SECONDARY],
                 labels={"AvgBalance": "Avg Balance (€)"})
    return _style(fig, "Average Balance by Geography & Churn Status")


def bar_credit_score_churn(df_cs):
    fig = px.bar(df_cs, x="CreditBand", y="ChurnRate",
                 color="ChurnRate",
                 color_continuous_scale=["#2ECC71", "#F39C12", "#E74C3C"],
                 text="ChurnRate", labels={"ChurnRate": "Churn Rate (%)"})
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_coloraxes(showscale=False)
    return _style(fig, "Churn Rate by Credit Score Band")


def bar_rsi_churn(df_rsi):
    fig = px.bar(df_rsi, x="RSI_Tier", y="ChurnRate",
                 color="RSI_Tier", color_discrete_sequence=PALETTE,
                 text="ChurnRate", labels={"ChurnRate": "Churn Rate (%)"})
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    return _style(fig, "Churn Rate by Relationship Strength Index Tier")


def bar_tier_retention(df_tier):
    fig = px.bar(df_tier, x="EngagementTier", y="RetentionRate",
                 color="EngagementTier", color_discrete_sequence=PALETTE,
                 text="RetentionRate", labels={"RetentionRate": "Retention Rate (%)"})
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    return _style(fig, "Retention Rate by Engagement Tier")


def line_threshold_churn(df_thresh):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_thresh["Threshold"], y=df_thresh["Above_ChurnRate"],
                             mode="lines+markers", name="Score ≥ Threshold",
                             line=dict(color=ACCENT, width=2.5)))
    fig.add_trace(go.Scatter(x=df_thresh["Threshold"], y=df_thresh["Below_ChurnRate"],
                             mode="lines+markers", name="Score < Threshold",
                             line=dict(color=SECONDARY, width=2.5, dash="dash")))
    fig.update_layout(xaxis_title="Relationship Score Threshold", yaxis_title="Churn Rate (%)")
    return _style(fig, "Churn Rate vs Engagement Score Threshold", height=420)


def gauge_chart(value, title, max_val=100, low=25, high=45):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value,
        title={"text": title, "font": {"size": 13}},
        gauge={
            "axis": {"range": [0, max_val]}, "bar": {"color": PRIMARY},
            "steps": [
                {"range": [0, low],       "color": "#D5F5E3"},
                {"range": [low, high],    "color": "#FAD7A0"},
                {"range": [high, max_val],"color": "#FADBD8"},
            ],
            "threshold": {"line": {"color": "red", "width": 3}, "value": high},
        },
    ))
    fig.update_layout(height=220, margin=dict(l=20, r=20, t=40, b=10),
                      paper_bgcolor="rgba(0,0,0,0)")
    return fig
