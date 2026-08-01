"""
liquidity_risk.py

Functions for calculating Liquidity Risk metrics.
"""

import pandas as pd


LIQUID_ASSET_CATEGORIES = {"Cash", "Securities"}


def calculate_liquid_assets(df: pd.DataFrame) -> float:
    """
    Calculate total short-term liquid assets.
    """

    liquid_assets = df[
        (df["side"] == "asset")
        & (df["maturity"] == "short")
        & (df["category"].isin(LIQUID_ASSET_CATEGORIES))
    ]["amount"].sum()

    return float(liquid_assets)


def calculate_short_term_liabilities(df: pd.DataFrame) -> float:
    """
    Calculate total short-term liabilities.
    """

    liabilities = df[
        (df["side"] == "liability")
        & (df["maturity"] == "short")
    ]["amount"].sum()

    return float(liabilities)


def calculate_excess_liquidity(
    liquid_assets: float,
    short_term_liabilities: float
) -> float:
    """
    Excess Liquidity = Liquid Assets - Short-Term Liabilities
    """

    return liquid_assets - short_term_liabilities


def calculate_coverage_ratio(
    liquid_assets: float,
    short_term_liabilities: float
) -> float:
    """
    Liquidity Coverage Ratio (Simplified)
    """

    if short_term_liabilities == 0:
        return float("inf")

    return liquid_assets / short_term_liabilities


def liquidity_summary(df: pd.DataFrame) -> dict:

    liquid_assets = calculate_liquid_assets(df)

    short_liabilities = calculate_short_term_liabilities(df)

    excess = calculate_excess_liquidity(
        liquid_assets,
        short_liabilities
    )

    coverage = calculate_coverage_ratio(
        liquid_assets,
        short_liabilities
    )

    return {
        "Liquid Assets": liquid_assets,
        "Short-Term Liabilities": short_liabilities,
        "Excess Liquidity": excess,
        "Coverage Ratio": coverage,
    }