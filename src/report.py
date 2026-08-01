from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors


def generate_pdf(capital, liquidity, interest, overall):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    clean_rating = (
        overall.replace("🟢", "")
        .replace("🟡", "")
        .replace("🔴", "")
        .strip()
    )

    story.append(
        Paragraph(
            "<b>Bank Balance Sheet Risk Dashboard Report</b>",
            styles["Title"],
        )
    )


    story.append(
        Paragraph(
            f"<b>Overall Risk Rating:</b> {clean_rating}",
            styles["Normal"],
        )
    )


    story.append(Spacer(1, 20))

    table_data = [
        ["Metric", "Value"],
        ["CET1 Ratio", f"{capital['CET1 Ratio']*100:.2f}%"],
        ["Coverage Ratio", f"{liquidity['Coverage Ratio']:.2f}"],
        ["Repricing Gap", f"{interest['Repricing Gap']:,.2f}"],
        ["Interest Rate Classification", interest["Classification"]],
]

    table = Table(table_data, colWidths=[220, 220])

    table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("TOPPADDING", (0, 1), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]
        )
    )

    story.append(table)

    doc.build(story)

    buffer.seek(0)

    return buffer