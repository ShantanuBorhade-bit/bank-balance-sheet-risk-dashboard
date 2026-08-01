import streamlit as st

from src.validation import (
    load_default_data,
    load_uploaded_data,
)
from src.actions import generate_actions
from src.capital_risk import capital_summary
from src.liquidity_risk import liquidity_summary
from src.interest_rate_risk import interest_rate_summary
from src.simulator import simulate_rate_shock
from src.dashboard import overall_risk
from src.recommendations import generate_summary
from src.charts import (
    capital_gauge,
    bar_chart,
    asset_allocation,
    liability_allocation,
)
from src.report import generate_pdf
from src.ui import (
    show_header,
    show_overall_risk,
    show_kpis,
)


# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Bank Balance Sheet Risk Dashboard",
    page_icon="🏦",
    layout="wide",
)


# --------------------------------------------------
# CSS
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
    type="csv",
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
    4.0,
    15.0,
    8.0,
)


# --------------------------------------------------
# Load Data
# --------------------------------------------------

try:

    if uploaded_file is not None:

        df = load_uploaded_data(uploaded_file)

        st.sidebar.success(
            "Custom balance sheet loaded."
        )

    else:

        df = load_default_data(
            "data/sample_balance_sheet.csv"
        )

        st.sidebar.info(
            "Using sample balance sheet."
        )

except Exception as e:

    st.error(str(e))
    st.stop()


# --------------------------------------------------
# Calculations
# --------------------------------------------------

capital = capital_summary(df)

liquidity = liquidity_summary(df)

interest = interest_rate_summary(df)

overall = overall_risk(
    capital,
    liquidity,
    interest,
    benchmark,
)

summary = generate_summary(
    capital,
    liquidity,
    interest,
    benchmark,
)

actions = generate_actions(
    capital,
    liquidity,
    interest,
    benchmark,
)

total_assets = (
    df[df["side"] == "asset"]["amount"].sum()
)


# --------------------------------------------------
# Header
# --------------------------------------------------

show_header()

show_overall_risk(overall)



cet1 = capital["CET1 Ratio"] * 100

if cet1 >= benchmark:
    st.success(
        f"✅ CET1 Ratio ({cet1:.2f}%) meets the selected benchmark ({benchmark:.2f}%)."
    )
else:
    st.error(
        f"❌ CET1 Ratio ({cet1:.2f}%) is below the selected benchmark ({benchmark:.2f}%)."
    )

st.subheader("📋 Executive Summary")

for point in summary:
    st.write(point)

st.divider()

st.subheader("💡 Recommended Actions")

for i, action in enumerate(actions, start=1):
    st.write(f"**{i}.** {action}")

st.divider()

show_kpis(
    capital,
    liquidity,
    interest,
    total_assets,
)

st.divider()


# --------------------------------------------------
# Tabs
# --------------------------------------------------

overview_tab, capital_tab, liquidity_tab, interest_tab, simulator_tab, report_tab = st.tabs(
    [
        "📊 Overview",
        "🏛 Capital Risk",
        "💧 Liquidity Risk",
        "📈 Interest Rate Risk",
        "⚡ Rate Shock Simulator",
        "📄 Report",
    ]
)


# --------------------------------------------------
# Overview
# --------------------------------------------------

with overview_tab:

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(
            asset_allocation(df),
            use_container_width=True,
        )

    with col2:

        st.plotly_chart(
            liability_allocation(df),
            use_container_width=True,
        )

    st.divider()

    st.subheader("Balance Sheet Data")

    st.dataframe(
        df,
        use_container_width=True,
    )


# --------------------------------------------------
# Capital Risk
# --------------------------------------------------

with capital_tab:

    left, right = st.columns([1, 2])

    with left:

        st.plotly_chart(
            capital_gauge(
                capital["CET1 Ratio"],
                benchmark,
            ),
            use_container_width=True,
        )

    with right:

        st.plotly_chart(
            bar_chart(
                ["CET1", "RWA"],
                [
                    capital["CET1"],
                    capital["RWA"],
                ],
                "Capital vs Risk Weighted Assets",
            ),
            use_container_width=True,
        )


# --------------------------------------------------
# Liquidity Risk
# --------------------------------------------------

with liquidity_tab:

    st.metric(
        "Coverage Ratio",
        f"{liquidity['Coverage Ratio']:.2f}x"
    )

    st.plotly_chart(
        bar_chart(
            [
                "Liquid Assets",
                "Short Liabilities",
            ],
            [
                liquidity["Liquid Assets"],
                liquidity["Short-Term Liabilities"],
            ],
            "Liquidity Coverage",
        ),
        use_container_width=True,
    )


# --------------------------------------------------
# Interest Rate Risk
# --------------------------------------------------

with interest_tab:

    st.metric(
        "Repricing Gap",
        f"{interest['Repricing Gap']:,.0f}"
    )

    st.caption(
        f"Classification: **{interest['Classification']}**"
    )

    st.plotly_chart(
        bar_chart(
            [
                "Short Assets",
                "Short Liabilities",
            ],
            [
                interest["Short Assets"],
                interest["Short Liabilities"],
            ],
            "Short-Term Repricing Gap",
        ),
        use_container_width=True,
    )
# --------------------------------------------------
# Rate Shock Simulator
# --------------------------------------------------

with simulator_tab:

    st.subheader("⚡ Interest Rate Shock Simulator")

    shock = st.slider(
        "Interest Rate Shock (Basis Points)",
        min_value=-300,
        max_value=300,
        value=0,
        step=25,
    )

    delta_nii = simulate_rate_shock(
        interest["Repricing Gap"],
        shock,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Rate Shock",
            f"{shock:+} bps",
        )

    with col2:
        st.metric(
            "Estimated Change in Net Interest Income",
            f"{delta_nii:,.2f}",
        )

    if delta_nii > 0:
        st.success(
            "The current balance sheet is expected to benefit from this interest rate scenario."
        )
    elif delta_nii < 0:
        st.warning(
            "The current balance sheet is expected to experience lower net interest income under this scenario."
        )
    else:
        st.info(
            "No change in estimated net interest income."
        )
# --------------------------------------------------
# Report
# --------------------------------------------------

with report_tab:

    st.subheader("📄 Export Report")

    pdf = generate_pdf(
        capital,
        liquidity,
        interest,
        overall,
    )

    st.download_button(
        label="📥 Download PDF Report",
        data=pdf,
        file_name="bank_risk_report.pdf",
        mime="application/pdf",
    )