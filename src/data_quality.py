import streamlit as st


def show_data_quality(df):

    st.subheader("🛡️ Data Quality Checks")

    issues = []

    if df.isnull().sum().sum() > 0:
        issues.append("Dataset contains missing values.")

    if (df["amount"] < 0).any():
        issues.append("Negative amounts detected.")

    if df.duplicated().any():
        issues.append("Duplicate records detected.")

    asset_total = df[df["side"] == "asset"]["amount"].sum()
    liability_total = (
        df[df["side"].isin(["liability", "equity"])]["amount"].sum()
    )

    if abs(asset_total - liability_total) > 1:
        issues.append(
            "Balance Sheet is not balanced (Assets ≠ Liabilities + Equity)."
        )

    if issues:
        for issue in issues:
            st.error(issue)
    else:
        st.success("No data quality issues detected.")