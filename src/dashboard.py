def overall_risk(capital, liquidity, interest):

    score = 0

    if capital["CET1 Ratio"] < 0.08:
        score += 2
    elif capital["CET1 Ratio"] < 0.10:
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