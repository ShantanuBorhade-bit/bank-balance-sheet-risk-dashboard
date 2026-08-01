"""
charts.py

Reusable charts for the dashboard.
"""

import matplotlib.pyplot as plt


def create_bar_chart(labels, values, title, ylabel):

    fig, ax = plt.subplots(figsize=(6,4))

    bars = ax.bar(labels, values)

    ax.set_title(title)
    ax.set_ylabel(ylabel)

    for bar in bars:

        height = bar.get_height()

        ax.text(
            bar.get_x()+bar.get_width()/2,
            height,
            f"{height:,.0f}",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()

    return fig


def create_pie_chart(labels, values, title):

    fig, ax = plt.subplots(figsize=(5,5))

    ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title(title)

    return fig