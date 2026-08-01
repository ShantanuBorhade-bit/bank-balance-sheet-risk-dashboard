def generate_summary(capital, liquidity, interest, benchmark):

    summary = []

    cet1 = capital["CET1 Ratio"] * 100

    if cet1 >= benchmark:
        summary.append(
            f"✔ CET1 Ratio ({cet1:.2f}%) is above the selected benchmark ({benchmark:.2f}%)."
        )
    else:
        summary.append(
            f"✖ CET1 Ratio ({cet1:.2f}%) is below the selected benchmark ({benchmark:.2f}%)."
        )

    if liquidity["Coverage Ratio"] >= 1:
        summary.append(
            "✔ Short-term liquidity appears sufficient to cover short-term obligations."
        )
    else:
        summary.append(
            "✖ Liquidity coverage is below 1. The bank may struggle to meet short-term obligations."
        )

    if interest["Classification"] == "Balanced":
        summary.append(
            "✔ Interest rate exposure is balanced."
        )

    elif interest["Classification"] == "Asset-sensitive":
        summary.append(
            "ℹ The bank is asset-sensitive. Rising interest rates may improve earnings."
        )

    else:
        summary.append(
            "ℹ The bank is liability-sensitive. Rising interest rates may reduce earnings."
        )

    return summary