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

    fig.update_layout(
    height=350,
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(size=16),
)

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
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=400,
    showlegend=False,
    title_x=0.5,
    margin=dict(l=20, r=20, t=60, b=20),
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

    fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    height=420,
    title_x=0.5,
    legend_orientation="h",
    legend_y=-0.15,
)

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

def risk_overview(capital, liquidity, interest):

    labels = [
        "CET1 Ratio (%)",
        "Coverage Ratio",
        "Repricing Gap",
    ]

    values = [
        capital["CET1 Ratio"] * 100,
        liquidity["Coverage Ratio"],
        abs(interest["Repricing Gap"]) / 1000,
    ]

    fig = px.bar(
        x=labels,
        y=values,
        text=[f"{v:.2f}" for v in values],
        color=labels,
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        title="Overall Risk Indicators",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        title_x=0.5,
        height=420,
    )

    return fig

def shock_analysis_chart(repricing_gap, selected_shock):

    import plotly.graph_objects as go

    shocks = [-300, -200, -100, 0, 100, 200, 300]

    values = [
        repricing_gap * (bps / 10000)
        for bps in shocks
    ]

    selected_value = repricing_gap * (selected_shock / 10000)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=shocks,
            y=values,
            mode="lines+markers",
            name="Sensitivity Curve",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[selected_shock],
            y=[selected_value],
            mode="markers",
            marker=dict(size=14, color="red"),
            name="Selected Shock",
        )
    )

    fig.update_layout(
        title="Net Interest Income Sensitivity",
        xaxis_title="Interest Rate Shock (bps)",
        yaxis_title="Estimated Change in NII",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title_x=0.5,
        height=420,
    )

    return fig

