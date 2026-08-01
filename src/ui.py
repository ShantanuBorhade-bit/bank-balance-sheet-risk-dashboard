import streamlit as st


import streamlit as st
from datetime import datetime


def show_header():

    col1, col2 = st.columns([4, 1])

    with col1:
        st.title("🏦 Bank Balance Sheet Risk Dashboard")
        st.caption(
            "Capital Risk • Liquidity Risk • Interest Rate Risk"
        )

    with col2:
        st.metric(
            "Generated",
            datetime.now().strftime("%d-%b-%Y"),
        )

    st.divider()


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

def show_scorecard(capital, liquidity, interest, benchmark):

    st.subheader("📊 Risk Scorecard")

    c1, c2, c3 = st.columns(3)

    cet1 = capital["CET1 Ratio"] * 100

    with c1:
        if cet1 >= benchmark:
            st.success("🟢 Capital Position\n\nHealthy")
        else:
            st.error("🔴 Capital Position\n\nBelow Benchmark")

    with c2:
        if liquidity["Coverage Ratio"] >= 1:
            st.success("🟢 Liquidity\n\nAdequate")
        else:
            st.error("🔴 Liquidity\n\nInsufficient")

    with c3:
        if interest["Classification"] == "Balanced":
            st.success("🟢 Interest Rate Risk\n\nBalanced")
        else:
            st.warning(
                f"🟡 {interest['Classification']}"
            )

    st.divider()

def show_statistics(df):

    st.subheader("📈 Balance Sheet Statistics")

    total_assets = df[df["side"] == "asset"]["amount"].sum()

    total_liabilities = df[df["side"] == "liability"]["amount"].sum()

    total_equity = df[df["side"] == "equity"]["amount"].sum()

    records = len(df)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Assets", f"{total_assets:,.0f}")

    c2.metric("Liabilities", f"{total_liabilities:,.0f}")

    c3.metric("Equity", f"{total_equity:,.0f}")

    c4.metric("Records", records)

def show_dashboard_summary(df, capital, liquidity, interest):

    assets = df[df["side"] == "asset"]["amount"].sum()
    liabilities = df[df["side"] == "liability"]["amount"].sum()
    equity = df[df["side"] == "equity"]["amount"].sum()

    st.subheader("🏦 Executive Dashboard")

    left, right = st.columns(2)

    with left:

        st.markdown("### Balance Sheet")

        st.write(f"**Total Assets** : {assets:,.0f}")
        st.write(f"**Total Liabilities** : {liabilities:,.0f}")
        st.write(f"**Total Equity** : {equity:,.0f}")
        st.write(f"**Records** : {len(df)}")

    with right:

        st.markdown("### Risk Snapshot")

        st.write(f"**CET1 Ratio** : {capital['CET1 Ratio']*100:.2f}%")
        st.write(f"**Coverage Ratio** : {liquidity['Coverage Ratio']:.2f}x")
        st.write(f"**Interest Position** : {interest['Classification']}")