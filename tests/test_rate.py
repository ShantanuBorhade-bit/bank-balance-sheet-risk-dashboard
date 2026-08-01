import pandas as pd

from src.interest_rate_risk import interest_rate_summary

df = pd.read_csv("data/sample_balance_sheet.csv")

print(interest_rate_summary(df))