"""
interest_rate_risk.py

Functions for calculating Interest Rate Risk
using a simplified repricing gap model.
"""

import pandas as pd


def calculate_short_term_assets(df: pd.DataFrame) -> float:
    """Calculate total short-term assets."""

    return float(
        df[
            (df["side"] == "asset") &
            (df["maturity"] == "short")
        ]["amount"].sum()
    )


def calculate_short_term_liabilities(df: pd.DataFrame) -> float:
    """Calculate total short-term liabilities."""

    return float(
        df[
            (df["side"] == "liability") &
            (df["maturity"] == "short")
        ]["amount"].sum()
    )


def calculate_long_term_assets(df: pd.DataFrame) -> float:
    """Calculate total long-term assets."""

    return float(
        df[
            (df["side"] == "asset") &
            (df["maturity"] == "long")
        ]["amount"].sum()
    )


def calculate_long_term_liabilities(df: pd.DataFrame) -> float:
    """Calculate total long-term liabilities."""

    return float(
        df[
            (df["side"] == "liability") &
            (df["maturity"] == "long")
        ]["amount"].sum()
    )


def calculate_repricing_gap(
    short_assets: float,
    short_liabilities: float
) -> float:
    """
    Repricing Gap = Short-Term Assets - Short-Term Liabilities
    """

    return short_assets - short_liabilities


def classify_interest_rate_risk(repricing_gap: float) -> str:

    if repricing_gap > 0:
        return "Asset-sensitive"

    if repricing_gap < 0:
        return "Liability-sensitive"

    return "Balanced"


def interest_rate_summary(df: pd.DataFrame):

    short_assets = calculate_short_term_assets(df)
    short_liabilities = calculate_short_term_liabilities(df)

    long_assets = calculate_long_term_assets(df)
    long_liabilities = calculate_long_term_liabilities(df)

    gap = calculate_repricing_gap(
        short_assets,
        short_liabilities
    )

    return {
        "Short Assets": short_assets,
        "Short Liabilities": short_liabilities,
        "Long Assets": long_assets,
        "Long Liabilities": long_liabilities,
        "Repricing Gap": gap,
        "Classification": classify_interest_rate_risk(gap)
    }