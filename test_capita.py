import pandas as pd

from src.capital_risk import capital_summary

df = pd.read_csv("data/sample_balance_sheet.csv")

result = capital_summary(df)

print(result)