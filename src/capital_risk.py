"""
capital_risk.py
Functions for calculating Capital Risk metrics
for the Bank Balance Sheet Risk Dashboard.
"""

import pandas as pd


def calculate_rwa(df: pd.DataFrame) -> float:
    """
    Calculate Risk Weighted Assets (RWA).

    Formula:
        RWA = Σ (Asset Amount × Risk Weight)
    """

    assets = df[df["side"] == "asset"].copy()

    assets["risk_weight"] = assets["risk_weight"].fillna(1.0)

    rwa = (assets["amount"] * assets["risk_weight"]).sum()

    return float(rwa)


def calculate_cet1(df: pd.DataFrame) -> float:
    """
    Return CET1 Capital.
    """

    equity = df[df["side"] == "equity"]

    cet1 = equity[
        equity["item"].str.contains("CET1", case=False, na=False)
    ]["amount"].sum()

    return float(cet1)


def calculate_cet1_ratio(cet1: float, rwa: float) -> float:
    """
    Calculate CET1 Ratio.

    Formula:
        CET1 Ratio = CET1 / RWA
    """

    if rwa == 0:
        return 0.0

    return cet1 / rwa


def capital_summary(df: pd.DataFrame) -> dict:
    """
    Returns all capital metrics in one dictionary.
    """

    rwa = calculate_rwa(df)

    cet1 = calculate_cet1(df)

    ratio = calculate_cet1_ratio(cet1, rwa)

    return {
        "RWA": rwa,
        "CET1": cet1,
        "CET1 Ratio": ratio,
    }