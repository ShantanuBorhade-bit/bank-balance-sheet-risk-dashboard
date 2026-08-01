"""
validation.py

Data loading and validation utilities.
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


def validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate the structure of a balance sheet DataFrame.
    """

    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(sorted(missing))
        )

    df["side"] = (
        df["side"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    df["maturity"] = (
        df["maturity"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df["risk_weight"] = pd.to_numeric(
        df["risk_weight"],
        errors="coerce"
    )

    if df["amount"].isna().any():
        raise ValueError(
            "Column 'amount' contains invalid values."
        )

    return df


def load_default_data(filepath: str) -> pd.DataFrame:
    """
    Load the default CSV.
    """

    df = pd.read_csv(filepath)

    return validate_dataframe(df)


def load_uploaded_data(uploaded_file) -> pd.DataFrame:
    """
    Load an uploaded CSV file.
    """

    df = pd.read_csv(uploaded_file)

    return validate_dataframe(df)