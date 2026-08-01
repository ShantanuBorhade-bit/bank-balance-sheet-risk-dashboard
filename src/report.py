"""
report.py

Functions for exporting dashboard reports.
"""

import json


def export_json(report: dict):

    return json.dumps(
        report,
        indent=4
    )