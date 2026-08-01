import streamlit as st


def show_header():
    st.title("🏦 Bank Balance Sheet Risk Dashboard")
    st.caption(
        "Analyze Capital Risk, Liquidity Risk, and Interest Rate Risk."
    )


def show_overall_risk(rating):
    st.success(f"Overall Risk Rating: {rating}")


def show_kpis(capital, liquidity, interest, total_assets):

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "CET1 Ratio",
        f"{capital['CET1 Ratio']*100:.2f}%"
    )

    c2.metric(
        "Coverage Ratio",
        f"{liquidity['Coverage Ratio']:.2f}x"
    )

    c3.metric(
        "Repricing Gap",
        f"{interest['Repricing Gap']:,.0f}"
    )

    c4.metric(
        "Total Assets",
        f"{total_assets:,.0f}"
    )