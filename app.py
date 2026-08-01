import streamlit as st

from src.validation import (
    load_default_data,
    load_uploaded_data,
)

from src.capital_risk import capital_summary
from src.liquidity_risk import liquidity_summary
from src.interest_rate_risk import interest_rate_summary
from src.dashboard import overall_risk
from src.utils import risk_status
from src.charts import create_bar_chart


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Bank Balance Sheet Risk Dashboard",
    page_icon="🏦",
    layout="wide",
)


# --------------------------------------------------
# Load Custom CSS
# --------------------------------------------------

def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True,
            )
    except FileNotFoundError:
        pass


load_css()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("🏦 Dashboard")

uploaded_file = st.sidebar.file_uploader(
    "Upload Balance Sheet CSV",
    type=["csv"],
)

with st.sidebar.expander("Expected CSV Format"):

    st.code(
        """side,category,item,amount,maturity,risk_weight
asset,Loans,Retail Loans,250000,long,0.75
liability,Deposits,Savings Deposits,300000,short,
equity,Capital,CET1 Capital,180000,long,
"""
    )

benchmark = st.sidebar.slider(
    "Minimum CET1 Benchmark (%)",
    min_value=4.0,
    max_value=15.0,
    value=8.0,
)


# --------------------------------------------------
# Load Data
# --------------------------------------------------

try:

    if uploaded_file is not None:

        df = load_uploaded_data(uploaded_file)

        st.sidebar.success(
            "✅ Custom balance sheet loaded."
        )

    else:

        df = load_default_data(
            "data/sample_balance_sheet.csv"
        )

        st.sidebar.info(
            "Using sample dataset."
        )

except Exception as e:

    st.error(str(e))

    st.stop()


# --------------------------------------------------
# Calculate Metrics
# --------------------------------------------------

capital = capital_summary(df)
liquidity = liquidity_summary(df)
interest = interest_rate_summary(df)

overall = overall_risk(
    capital,
    liquidity,
    interest,
)

total_assets = (
    df[df["side"] == "asset"]["amount"].sum()
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🏦 Bank Balance Sheet Risk Dashboard")

st.markdown(
"""
Analyze a bank balance sheet across:

- Capital Risk
- Liquidity Risk
- Interest Rate Risk

using simplified educational risk models.
"""
)

st.divider()


# --------------------------------------------------
# Overall Risk
# --------------------------------------------------

st.success(
    f"### Overall Risk Rating : {overall}"
)


# --------------------------------------------------
# Executive Summary
# --------------------------------------------------

st.subheader("📋 Executive Summary")

capital_status = risk_status(
    capital["CET1 Ratio"] * 100,
    8,
    10,
)

liquidity_status = (
    "🟢 Healthy"
    if liquidity["Excess Liquidity"] >= 0
    else "🔴 Shortfall"
)

interest_status = (
    "🟢 Balanced"
    if interest["Classification"] == "Balanced"
    else "🟡 Monitor"
)

st.info(
f"""
**Capital Risk:** {capital_status}

**Liquidity Risk:** {liquidity_status}

**Interest Rate Risk:** {interest_status}
"""
)


# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "CET1 Ratio",
    f"{capital['CET1 Ratio']*100:.2f}%"
)

col2.metric(
    "Coverage Ratio",
    f"{liquidity['Coverage Ratio']:.2f}x"
)

col3.metric(
    "Repricing Gap",
    f"{interest['Repricing Gap']:,.0f}"
)

col4.metric(
    "Total Assets",
    f"{total_assets:,.0f}"
)

st.divider()


# --------------------------------------------------
# Tabs
# --------------------------------------------------

overview_tab, capital_tab, liquidity_tab, interest_tab = st.tabs(
    [
        "📊 Overview",
        "🏛️ Capital Risk",
        "💧 Liquidity Risk",
        "📈 Interest Rate Risk",
    ]
)


# --------------------------------------------------
# Overview
# --------------------------------------------------

with overview_tab:

    st.subheader("Balance Sheet Dataset")

    st.dataframe(
        df,
        use_container_width=True,
    )


# --------------------------------------------------
# Capital Risk
# --------------------------------------------------

with capital_tab:

    st.subheader("🏛️ Capital Risk")

    st.metric(
        "CET1 Ratio",
        f"{capital['CET1 Ratio']*100:.2f}%"
    )

    fig = create_bar_chart(
        ["CET1", "RWA"],
        [
            capital["CET1"],
            capital["RWA"],
        ],
        "Capital vs Risk Weighted Assets",
        "Amount",
    )

    st.pyplot(fig)


# --------------------------------------------------
# Liquidity Risk
# --------------------------------------------------

with liquidity_tab:

    st.subheader("💧 Liquidity Risk")

    st.metric(
        "Coverage Ratio",
        f"{liquidity['Coverage Ratio']:.2f}x"
    )

    fig = create_bar_chart(
        [
            "Liquid Assets",
            "Short Liabilities",
        ],
        [
            liquidity["Liquid Assets"],
            liquidity["Short-Term Liabilities"],
        ],
        "Liquidity Coverage",
        "Amount",
    )

    st.pyplot(fig)


# --------------------------------------------------
# Interest Rate Risk
# --------------------------------------------------

with interest_tab:

    st.subheader("📈 Interest Rate Risk")

    st.metric(
        "Repricing Gap",
        f"{interest['Repricing Gap']:,.0f}"
    )

    st.write(
        f"**Classification:** {interest['Classification']}"
    )

    fig = create_bar_chart(
        [
            "Short Assets",
            "Short Liabilities",
        ],
        [
            interest["Short Assets"],
            interest["Short Liabilities"],
        ],
        "Short-Term Repricing Gap",
        "Amount",
    )

    st.pyplot(fig)