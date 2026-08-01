"""
charts.py

Reusable plotting functions.
"""

import matplotlib.pyplot as plt


def create_bar_chart(
    labels,
    values,
    title,
    ylabel,
):

    fig, ax = plt.subplots(figsize=(6,4))

    ax.bar(labels, values)

    ax.set_title(title)

    ax.set_ylabel(ylabel)

    for i, value in enumerate(values):
        ax.text(
            i,
            value,
            f"{value:,.0f}",
            ha="center",
            va="bottom",
        )

    return fig