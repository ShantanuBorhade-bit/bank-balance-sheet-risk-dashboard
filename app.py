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
    risk_overview,
    shock_analysis_chart,
)
from src.report import generate_pdf
from src.ui import (
    show_header,
    show_overall_risk,
    show_kpis,
    show_scorecard,
    show_statistics,
    show_dashboard_summary,
)
from src.data_quality import show_data_quality

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

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🏦 Bank Risk Dashboard")

st.sidebar.markdown("---")

# ---------------------------
# Data
# ---------------------------

with st.sidebar.expander("📂 Data", expanded=True):

    uploaded_file = st.file_uploader(
        "Upload Balance Sheet CSV",
        type=["csv"],
    )

    if uploaded_file is None:
        st.info("Using sample dataset")
    else:
        st.success("Custom dataset loaded")

# ---------------------------
# Risk Settings
# ---------------------------

with st.sidebar.expander("🎯 Risk Settings", expanded=True):

    benchmark = st.slider(
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


    else:

        df = load_default_data(
            "data/sample_balance_sheet.csv"
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

# ---------------------------
# Dashboard Info
# ---------------------------

with st.sidebar.expander("📊 Dashboard Info", expanded=False):

    st.metric("Records", len(df))

    st.metric(
        "Overall Risk",
        overall.replace("🟢", "").replace("🟡", "").replace("🔴", "").strip(),
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


# ---------------------------
# Help
# ---------------------------

with st.sidebar.expander("ℹ About"):

    st.markdown(
        """
**Bank Balance Sheet Risk Dashboard**

Version **1.0**

Built using:

- Streamlit
- Plotly
- Pandas
- ReportLab
"""
    )

# --------------------------------------------------
# Header
# --------------------------------------------------

show_header()

show_overall_risk(overall)



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

    cet1 = capital["CET1 Ratio"] * 100

    # ==========================================
    # Row 1
    # ==========================================

    left, right = st.columns([2, 1], gap="large")

    with left:

        show_dashboard_summary(
            df,
            capital,
            liquidity,
            interest,
        )

        st.markdown("### 📋 Executive Summary")

        for point in summary:
            st.write(f"• {point}")

        st.markdown("### 💡 Recommended Actions")

        for action in actions:
            st.write(f"✓ {action}")

    with right:

        show_scorecard(
            capital,
            liquidity,
            interest,
            benchmark,
        )

        if cet1 >= benchmark:
            st.success("Capital benchmark satisfied.")
        else:
            st.error("Capital benchmark not satisfied.")

        show_data_quality(df)

    st.divider()

    # ==========================================
    # Row 2
    # ==========================================

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

    # ==========================================
    # Dataset
    # ==========================================

    with st.expander("📄 Balance Sheet Data", expanded=False):

        c1, c2 = st.columns(2)

        with c1:

            side_filter = st.selectbox(
                "Filter by Side",
                ["All"] + sorted(df["side"].unique()),
            )

        with c2:

            search = st.text_input(
                "Search Item",
                placeholder="Search...",
            )

        filtered_df = df.copy()

        if side_filter != "All":
            filtered_df = filtered_df[
                filtered_df["side"] == side_filter
            ]

        if search:
            filtered_df = filtered_df[
                filtered_df["item"].str.contains(
                    search,
                    case=False,
                    na=False,
                )
            ]

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
        )

        csv = filtered_df.to_csv(index=False).encode()

        st.download_button(
            "📥 Download Filtered CSV",
            csv,
            "filtered_balance_sheet.csv",
            "text/csv",
        )

        st.caption(
            f"Showing {len(filtered_df)} of {len(df)} records."
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

    st.plotly_chart(
    shock_analysis_chart(
        interest["Repricing Gap"],
        shock,
    ),
    use_container_width=True,
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