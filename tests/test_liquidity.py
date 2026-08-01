import pandas as pd

from src.liquidity_risk import liquidity_summary

df = pd.read_csv("data/sample_balance_sheet.csv")

print(liquidity_summary(df))