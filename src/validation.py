"""
validation.py

Functions for loading and validating balance sheet data.
"""

import pandas as pd

REQUIRED_COLUMNS = {
    "side",
    "category",
    "item",
    "amount",
    "maturity",
    "risk_weight",
}


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load CSV into a DataFrame.
    """
    return pd.read_csv(filepath)


def validate_dataframe(df: pd.DataFrame):
    """
    Validate the uploaded balance sheet.
    """

    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing))}"
        )

    df["side"] = df["side"].str.lower().str.strip()
    df["maturity"] = df["maturity"].str.lower().str.strip()

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df["risk_weight"] = pd.to_numeric(
        df["risk_weight"],
        errors="coerce"
    )

    if df["amount"].isna().any():
        raise ValueError("Invalid amount values.")

    return df