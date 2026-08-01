"""
charts.py

Reusable Plotly charts for the Bank Balance Sheet Risk Dashboard.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


# --------------------------------------------------------
# Capital Risk
# --------------------------------------------------------

def capital_gauge(cet1_ratio: float, benchmark: float = 8):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=cet1_ratio * 100,
            number={"suffix": "%"},
            title={"text": "CET1 Ratio"},
           gauge={
    "axis": {"range": [0, 20]},
    "bar": {"color": "#1f77b4"},
    "threshold": {
        "line": {
            "color": "red",
            "width": 4,
        },
        "thickness": 0.8,
        "value": benchmark,
    },
    "steps": [
        {
            "range": [0, benchmark],
            "color": "#ffb3b3",
        },
        {
            "range": [benchmark, 20],
            "color": "#b8f2c8",
        },
    ],
},
        )
    )

    fig.update_layout(height=350)

    return fig


# --------------------------------------------------------
# Generic Bar Chart
# --------------------------------------------------------

def bar_chart(labels, values, title, yaxis="Amount"):

    fig = px.bar(
        x=labels,
        y=values,
        text=values,
        labels={"x": "", "y": yaxis},
        title=title,
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        height=400,
        showlegend=False,
    )

    return fig


# --------------------------------------------------------
# Donut Chart
# --------------------------------------------------------

def donut_chart(labels, values, title):

    fig = px.pie(
        names=labels,
        values=values,
        hole=0.55,
        title=title,
    )

    fig.update_layout(height=420)

    return fig


# --------------------------------------------------------
# Asset Allocation
# --------------------------------------------------------

def asset_allocation(df: pd.DataFrame):

    assets = (
        df[df["side"] == "asset"]
        .groupby("category")["amount"]
        .sum()
    )

    return donut_chart(
        assets.index,
        assets.values,
        "Asset Allocation",
    )


# --------------------------------------------------------
# Liability Allocation
# --------------------------------------------------------

def liability_allocation(df: pd.DataFrame):

    liabilities = (
        df[df["side"].isin(["liability", "equity"])]
        .groupby("category")["amount"]
        .sum()
    )

    return donut_chart(
        liabilities.index,
        liabilities.values,
        "Funding Structure",
    )