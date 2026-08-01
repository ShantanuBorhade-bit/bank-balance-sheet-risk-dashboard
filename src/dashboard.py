def overall_risk(capital, liquidity, interest, benchmark=8.0):
    """
    benchmark is the minimum acceptable CET1 Ratio in %
    """

    score = 0

    cet1 = capital["CET1 Ratio"] * 100

    if cet1 < benchmark:
        score += 2
    elif cet1 < benchmark + 2:
        score += 1

    if liquidity["Coverage Ratio"] < 1:
        score += 2
    elif liquidity["Coverage Ratio"] < 1.2:
        score += 1

    if interest["Classification"] != "Balanced":
        score += 1

    if score <= 1:
        return "🟢 LOW"

    if score <= 3:
        return "🟡 MEDIUM"

    return "🔴 HIGH"