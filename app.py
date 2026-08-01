import streamlit as st

from src.validation import load_data, validate_dataframe
from src.capital_risk import capital_summary
from src.liquidity_risk import liquidity_summary
from src.interest_rate_risk import interest_rate_summary
from src.dashboard import overall_risk
from src.utils import risk_status
from src.charts import create_bar_chart


# --------------------------------------------------
# Load Custom CSS
# --------------------------------------------------

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Bank Balance Sheet Risk Dashboard",
    page_icon="🏦",
    layout="wide",
)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

try:
    df = load_data("data/sample_balance_sheet.csv")
    df = validate_dataframe(df)

except Exception as e:
    st.error(f"Error loading dataset: {e}")
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
    interest
)

total_assets = df[df["side"] == "asset"]["amount"].sum()

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🏦 Bank Balance Sheet Risk Dashboard")

st.markdown(
"""
Analyze a bank's balance sheet across **Capital Risk,
Liquidity Risk, and Interest Rate Risk**
using simplified financial risk metrics.
"""
)

st.divider()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("Dashboard")

st.sidebar.success("✅ Sample Balance Sheet Loaded")

benchmark = st.sidebar.slider(
    "Minimum CET1 Benchmark (%)",
    4.0,
    15.0,
    8.0,
)

# --------------------------------------------------
# Overall Risk Rating
# --------------------------------------------------

st.success(f"### Overall Risk Rating : {overall}")

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

with col1:
    st.metric(
        "CET1 Ratio",
        f"{capital['CET1 Ratio']*100:.2f}%"
    )

with col2:
    st.metric(
        "Coverage Ratio",
        f"{liquidity['Coverage Ratio']:.2f}x"
    )

with col3:
    st.metric(
        "Repricing Gap",
        f"{interest['Repricing Gap']:,.0f}"
    )

with col4:
    st.metric(
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
            capital["RWA"]
        ],
        "Capital vs Risk Weighted Assets",
        "Amount"
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
            "Short Liabilities"
        ],
        [
            liquidity["Liquid Assets"],
            liquidity["Short-Term Liabilities"]
        ],
        "Liquidity Coverage",
        "Amount"
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
            "Short Liabilities"
        ],
        [
            interest["Short Assets"],
            interest["Short Liabilities"]
        ],
        "Short-Term Repricing Gap",
        "Amount"
    )

    st.pyplot(fig)