# 🏦 Customer Engagement & Product Utilization Analytics for Retention Strategy

> **Unified Mentor Project — European Central Bank**
> A complete data analytics project that identifies why customers leave a bank
> and what the bank can do to retain them — using real behavioural data.

---

## 📌 Table of Contents

1. [Project Background](#1-project-background)
2. [Problem Statement](#2-problem-statement)
3. [Project Objectives](#3-project-objectives)
4. [Dataset Description](#4-dataset-description)
5. [Project Structure](#5-project-structure)
6. [File Purpose Guide](#6-file-purpose-guide)
7. [Analytical Methodology](#7-analytical-methodology)
8. [Key Performance Indicators](#8-key-performance-indicators-kpis)
9. [Real Data Findings](#9-real-data-findings)
10. [Dashboard Modules](#10-dashboard-modules)
11. [Setup & Installation](#11-setup--installation)
12. [How to Run](#12-how-to-run)
13. [How Files Connect](#13-how-files-connect)
14. [Deliverables](#14-deliverables)
15. [Strategic Recommendations](#15-strategic-recommendations)
16. [Technologies Used](#16-technologies-used)

---

## 1. Project Background

Banks increasingly recognise that **customer behaviour and engagement** — not just
financial strength — determine long-term retention. A customer may have a high balance
or salary yet still churn due to:

- Low engagement with the bank's services
- Limited product adoption
- Weak relationship depth

This project evaluates customer retention through the lens of **behavioural engagement**
and **product utilisation** rather than demographics, providing a foundation for
data-driven cross-sell strategies, loyalty programmes, and retention initiatives.

**Unified Mentor:** European Central Bank
**Dataset Year:** 2025
**Dataset Size:** 10,000 customers across France, Spain, and Germany

---

## 2. Problem Statement

Despite having data on customer engagement and product usage, banks often lack:

- Quantitative insight into which behaviours actually drive retention
- Clarity on whether product depth reduces churn
- Evidence on whether high balances alone ensure loyalty

As a result, retention strategies are frequently **generic and misaligned** with
actual customer behaviour, leading to preventable churn.

---

## 3. Project Objectives

### Primary Objectives
- Evaluate the relationship between **engagement** and **churn**
- Measure the retention impact of **product count** and **product mix**
- Identify **disengaged yet high-value** customers at silent churn risk

### Secondary Objectives
- Support engagement-driven retention strategy design
- Improve product bundling decisions
- Reduce silent churn among premium customers

---

## 4. Dataset Description

**File:** `bank_churn.csv` (European_Bank.csv — Year 2025)
**Rows:** 10,000 customers | **Columns:** 14 | **Missing Values:** 0

| Column | Type | Description |
|---|---|---|
| `Year` | int | Dataset year (2025) |
| `CustomerId` | int | Unique customer identifier |
| `Surname` | str | Customer surname |
| `CreditScore` | int | Creditworthiness score (350–850) |
| `Geography` | str | Country: France / Spain / Germany |
| `Gender` | str | Male / Female |
| `Age` | int | Customer age (18–92) |
| `Tenure` | int | Years with the bank (0–10) |
| `Balance` | float | Account balance (€0 – €250,898) |
| `NumOfProducts` | int | Number of bank products held (1–4) |
| `HasCrCard` | int | Credit card ownership — 0 = No, 1 = Yes |
| `IsActiveMember` | int | Activity status — 0 = Inactive, 1 = Active |
| `EstimatedSalary` | float | Estimated annual salary (€) |
| `Exited` | int | **Churn target** — 0 = Retained, 1 = Churned |

---

## 5. Project Structure

```
UM-CUSTOMER_ANALYTICS/
│
├── pages/                          # Streamlit multi-page dashboard modules
│   ├── 01_Engagement_Overview.py   # Page 1 — Engagement vs Churn
│   ├── 02_Product_Utilization.py   # Page 2 — Product Utilization Impact
│   ├── 03_High_Value_Detector.py   # Page 3 — High-Value Customer Detector
│   └── 04_Retention_Scoring.py     # Page 4 — Retention Strength Scoring
│
├── app.py                          # Main Streamlit home page (entry point)
├── bank_churn.csv                  # Raw dataset (10,000 customers)
│
├── data_loader.py                  # Step 1 — Data ingestion & validation
├── engagement.py                   # Step 2 — Engagement classification
├── product_analysis.py             # Step 3 — Product utilization analysis
├── financial_analysis.py           # Step 4 — Financial vs engagement analysis
├── retention.py                    # Step 5 — Retention strength assessment
├── kpi.py                          # Aggregated KPI computation
├── visualizations.py               # Reusable Plotly chart builders (16 charts)
│
├── generate_eda_report.py          # Script — generates eda_report.txt
├── executive_summary.py            # Script — generates executive_summary.txt
├── eda_report.txt                  # Output — full EDA research paper
└── executive_summary.txt           # Output — ECB stakeholder summary
```

---

## 6. File Purpose Guide

### 🏠 Entry Point
| File | Purpose |
|---|---|
| `app.py` | The **main home page**. Run this with `streamlit run app.py`. Displays the overall KPI strip, geography and gender distribution charts, navigation cards, and a raw data preview. |

### 📊 Dashboard Pages (`pages/`)
| File | Purpose |
|---|---|
| `01_Engagement_Overview.py` | Displays engagement profiles, the Engagement Retention Ratio gauges, gender churn gap, age group analysis, and tenure trend. Sidebar filters: Geography, Gender, Activity, Tenure. |
| `02_Product_Utilization.py` | Highlights the 3-product cliff (82.71% churn at 3 products). Shows churn by product count, activity heatmap, geography analysis, and credit card stickiness. |
| `03_High_Value_Detector.py` | Detects 621 at-risk premium customers. Shows balance-activity matrix, salary-balance scatter, mismatch analysis, and credit score bands. Includes CSV export button. |
| `04_Retention_Scoring.py` | Displays RSI tiers, sticky customer profiles, RSI score histogram, engagement threshold chart, and the complete KPI table. |

### ⚙️ Analytics Modules
| File | Purpose |
|---|---|
| `data_loader.py` | Loads `bank_churn.csv`, validates the 14-column schema, checks binary fields (0/1), handles any missing values, and casts correct data types. Returns a clean DataFrame. |
| `engagement.py` | Classifies every customer into one of 4 engagement profiles using IsActiveMember, NumOfProducts, and Balance. Computes the Engagement Retention Ratio (ERR) KPI. Also provides gender, age group, and tenure churn breakdowns. |
| `product_analysis.py` | Calculates churn rate by number of products (1–4), the Product Depth Index (PDI), Credit Card Stickiness Score, and geography-level product analysis. |
| `financial_analysis.py` | Segments customers by balance tier, detects salary-balance mismatches, identifies at-risk premium customers (high balance + high salary + inactive), and analyses credit score bands. |
| `retention.py` | Computes the Relationship Strength Index (RSI) as a 0–100 composite score. Defines "sticky" customers (active + 2 products + credit card + 3yr tenure). Analyses engagement thresholds. |
| `kpi.py` | Aggregates all 5 KPIs (ERR, PDI, CCSS, HBDR, RSI) from across the modules into one dictionary and table for the dashboard. |
| `visualizations.py` | Contains 16 reusable Plotly chart-building functions used across all pages — bar charts, heatmaps, scatter plots, gauge charts, pie charts, and line charts. |

### 📄 Report Scripts & Outputs
| File | Purpose |
|---|---|
| `generate_eda_report.py` | Run once to produce the full EDA research paper. Covers 8 sections: dataset overview, engagement, products, financials, retention, KPIs, insights, and conclusion. |
| `executive_summary.py` | Run once to produce a concise summary for ECB and government stakeholders. Covers key findings, scale of the problem, and 7 prioritised recommendations. |
| `eda_report.txt` | The generated EDA research paper — already produced and ready to submit. |
| `executive_summary.txt` | The generated executive summary — already produced and ready to submit. |

---

## 7. Analytical Methodology

The project follows a 5-step analytical pipeline:

```
Step 1 — Data Ingestion & Validation
         Load CSV → validate schema → check binary fields → fix missing values

Step 2 — Engagement Classification
         Assign 4 engagement profiles → compute RelationshipScore (0–100)

Step 3 — Product Utilization Analysis
         Churn by product count → single vs multi-product → heatmap → geography

Step 4 — Financial Commitment vs Engagement
         Balance segments → salary-balance mismatch → at-risk premium detection

Step 5 — Retention Strength Assessment
         RSI scoring → sticky customer profiling → engagement threshold analysis
```

---

## 8. Key Performance Indicators (KPIs)

| # | KPI Name | Description | Real Value |
|---|---|---|---|
| 1 | **Engagement Retention Ratio (ERR)** | How many times more likely inactive customers are to churn vs active | **1.88×** |
| 2 | **Product Depth Index (PDI)** | Avg products held by retained customers ÷ avg by churned | **1.047** |
| 3 | **Credit Card Stickiness Score (CCSS)** | Churn reduction (pp) from credit card ownership | **0.63 pp** |
| 4 | **High-Balance Disengagement Rate (HBDR)** | % of premium-balance customers who are inactive | **49.88%** |
| 5 | **Relationship Strength Index (RSI)** | Composite 0–100 engagement score per customer | **42.5 avg** |

---

## 9. Real Data Findings

### Overall
| Metric | Value |
|---|---|
| Total Customers | 10,000 |
| Churned Customers | 2,037 **(20.37%)** |
| Active Members | 5,151 (51.51%) |
| Inactive Members | 4,849 (48.49%) |
| Zero Balance Customers | 3,617 (36.2%) |

### Product Churn — The 3-Product Cliff ⚠️
| Products | Churn Rate |
|---|---|
| 1 Product | 27.71% |
| **2 Products** | **7.58%** ← optimal |
| 3 Products | 82.71% ← cliff |
| 4 Products | 100.00% ← critical |

### Geography Churn
| Geography | Churn Rate |
|---|---|
| Germany | **32.44%** |
| Spain | 16.67% |
| France | 16.15% |

### Gender Churn
| Gender | Churn Rate |
|---|---|
| Female | **25.07%** |
| Male | 16.46% |

### Retention Strength
| Segment | Churn Rate |
|---|---|
| **Sticky Customers** | **5.05%** |
| Non-Sticky Customers | 22.68% |
| **Retention Advantage** | **17.63 pp** |

---

## 10. Dashboard Modules

| Page | Sidebar Filters | Key Visuals |
|---|---|---|
| 🏠 **Home** | — | KPI strip, geography & gender stacked bars, data preview |
| 📊 **Engagement Overview** | Geography, Gender, Activity, Tenure | ERR gauges, 4-profile bar & pie, gender, age group, tenure line |
| 📦 **Product Utilization** | Geography, Gender, Product count | 3-product cliff bar, activity heatmap, geography churn, CC stickiness |
| 🔍 **High-Value Detector** | Balance %, Salary %, Geography, Gender | At-risk table (621 customers), CSV export, scatter, credit score bands |
| 🏆 **Retention Scoring** | Geography, Gender, Min RSI | KPI table, RSI tier bars, sticky analysis, RSI histogram, threshold line |

---

## 11. Setup & Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Install Dependencies

```bash
# Recommended — avoids build-from-source errors
pip install --only-binary=:all: streamlit pandas numpy plotly scipy scikit-learn openpyxl

# Or install from requirements file
pip install -r requirements.txt
```

### requirements.txt
```
streamlit==1.32.0
pandas==2.2.1
numpy==1.26.4
plotly==5.20.0
scikit-learn==1.4.1
scipy==1.13.0
openpyxl==3.1.2
```

---

## 12. How to Run

### Launch the Dashboard
```bash
# Navigate to the project folder
cd UM-CUSTOMER_ANALYTICS

# Run the Streamlit app
streamlit run app.py
```
Opens automatically at **http://localhost:8501**

### Generate the EDA Research Report
```bash
python generate_eda_report.py
```
Output saved to `eda_report.txt`

### Generate the Executive Summary
```bash
python executive_summary.py
```
Output saved to `executive_summary.txt`

---

## 13. How Files Connect

```
bank_churn.csv
      │
      ▼
data_loader.py ──────── loads & validates raw data
      │
      ▼
engagement.py ──────────────────────────────────┐
product_analysis.py ────────────────────────────┤
financial_analysis.py ──────────────────────────┤ analyse data
retention.py ───────────────────────────────────┤
kpi.py (aggregates all KPIs) ───────────────────┘
      │
      ▼
visualizations.py ─────── turns data into Plotly charts
      │
      ├──▶ app.py                     (Home page)
      ├──▶ 01_Engagement_Overview.py  (Page 1)
      ├──▶ 02_Product_Utilization.py  (Page 2)
      ├──▶ 03_High_Value_Detector.py  (Page 3)
      └──▶ 04_Retention_Scoring.py    (Page 4)
                    │
                    ▼
      generate_eda_report.py ──▶ eda_report.txt
      executive_summary.py   ──▶ executive_summary.txt
```

---

## 14. Deliverables

| # | Deliverable | File | Status |
|---|---|---|---|
| 1 | EDA Research Paper | `eda_report.txt` | ✅ Ready |
| 2 | Executive Summary (ECB) | `executive_summary.txt` | ✅ Ready |
| 3 | Streamlit Dashboard | `app.py` + `pages/` | ✅ Ready |
| 4 | Analytics Pipeline | `data_loader.py` → `kpi.py` | ✅ Ready |
| 5 | Visualizations Library | `visualizations.py` | ✅ Ready |

---

## 15. Strategic Recommendations

| Priority | Recommendation | Target | Impact |
|---|---|---|---|
| 🔴 P1 | Re-engage inactive members with personalised campaigns | 4,849 inactive customers | High |
| 🔴 P2 | Audit and redesign all 3+ product bundles | 326 customers on 3–4 products | High |
| 🟠 P3 | Premium silent churn prevention programme | 621 at-risk premium customers | High |
| 🟠 P4 | Germany-specific regional retention initiative | 2,509 German customers | Medium |
| 🟡 P5 | Gender-responsive engagement strategy | Female customer segment | Medium |
| 🟡 P6 | Credit card acquisition push | 2,945 non-card holders | Medium |
| 🟢 P7 | Integrate RSI scoring into CRM for live monitoring | All 10,000 customers | Long-term |

---

## 16. Technologies Used

| Technology | Purpose |
|---|---|
| **Python 3.12** | Core programming language |
| **Streamlit** | Interactive web dashboard framework |
| **Pandas** | Data manipulation and analysis |
| **NumPy** | Numerical computations |
| **Plotly** | Interactive charts and visualizations |
| **SciPy** | Statistical tests (Chi-squared, Point-biserial) |
| **Scikit-Learn** | Supporting ML utilities |

---

## 📬 Project Info

| Field | Detail |
|---|---|
| **Project Name** | Customer Engagement & Product Utilization Analytics for Retention Strategy |
| **Unified Mentor** | European Central Bank |
| **Dataset** | European_Bank.csv — Year 2025 |
| **Customers** | 10,000 across France, Spain, Germany |
| **Overall Churn Rate** | 20.37% |

---

*Built with Python · Streamlit · Plotly · Pandas · SciPy*
