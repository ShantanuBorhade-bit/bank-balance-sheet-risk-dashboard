"""
simulator.py

Interest Rate Shock Simulator
"""


def simulate_rate_shock(
    repricing_gap: float,
    shock_bps: int,
):
    """
    ΔNII ≈ Repricing Gap × ΔRate
    """

    delta_rate = shock_bps / 10000

    delta_nii = repricing_gap * delta_rate

    return delta_nii