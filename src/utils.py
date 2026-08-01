"""
Utility functions.
"""

def risk_status(value, low, medium):

    if value >= medium:
        return "🟢 Low Risk"

    if value >= low:
        return "🟡 Moderate Risk"

    return "🔴 High Risk"