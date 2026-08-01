def generate_actions(capital, liquidity, interest, benchmark):

    actions = []

    cet1 = capital["CET1 Ratio"] * 100

    if cet1 < benchmark:
        actions.append(
            "Increase CET1 capital or reduce risk-weighted assets to meet the selected benchmark."
        )

    if liquidity["Coverage Ratio"] < 1:
        actions.append(
            "Increase liquid assets or reduce short-term liabilities to improve liquidity coverage."
        )

    if interest["Classification"] == "Asset-sensitive":
        actions.append(
            "Monitor the impact of falling interest rates on net interest income."
        )

    elif interest["Classification"] == "Liability-sensitive":
        actions.append(
            "Monitor the impact of rising interest rates on funding costs."
        )

    if not actions:
        actions.append(
            "Current indicators suggest the balance sheet is within acceptable limits. Continue periodic monitoring."
        )

    return actions