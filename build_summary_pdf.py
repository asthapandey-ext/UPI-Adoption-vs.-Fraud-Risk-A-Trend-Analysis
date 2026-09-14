from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER

NAVY = colors.HexColor('#0D1B2A')
TEAL = colors.HexColor('#1B9AAA')
DARKGREY = colors.HexColor('#333333')
MIDGREY = colors.HexColor('#666666')
LIGHTGREY = colors.HexColor('#F2F2F2')

styles = getSampleStyleSheet()

title_style = ParagraphStyle('TitleCustom', parent=styles['Title'], fontSize=19, textColor=NAVY,
                              spaceAfter=2, alignment=TA_LEFT, fontName='Helvetica-Bold')
subtitle_style = ParagraphStyle('SubtitleCustom', parent=styles['Normal'], fontSize=10.5, textColor=MIDGREY,
                                 spaceAfter=10, alignment=TA_LEFT)
h2_style = ParagraphStyle('H2Custom', parent=styles['Heading2'], fontSize=12.5, textColor=TEAL,
                           spaceBefore=10, spaceAfter=4, fontName='Helvetica-Bold')
body_style = ParagraphStyle('BodyCustom', parent=styles['Normal'], fontSize=9.5, textColor=DARKGREY,
                             leading=13.5, alignment=TA_LEFT)
bullet_style = ParagraphStyle('BulletCustom', parent=body_style, leftIndent=12, bulletIndent=0, spaceAfter=3)
headline_style = ParagraphStyle('Headline', parent=styles['Normal'], fontSize=11, textColor=NAVY,
                                 leading=15, alignment=TA_LEFT, fontName='Helvetica-Bold')
footnote_style = ParagraphStyle('Footnote', parent=styles['Normal'], fontSize=7.5, textColor=MIDGREY, leading=10)
kpi_num_style = ParagraphStyle('KPINum', parent=styles['Normal'], fontSize=16, textColor=NAVY,
                                fontName='Helvetica-Bold', alignment=TA_CENTER)
kpi_label_style = ParagraphStyle('KPILabel', parent=styles['Normal'], fontSize=7.5, textColor=MIDGREY,
                                  alignment=TA_CENTER, leading=9)

doc = SimpleDocTemplate("upi_project_summary.pdf", pagesize=A4,
                         topMargin=16*mm, bottomMargin=14*mm, leftMargin=16*mm, rightMargin=16*mm)

story = []

# --- Header ---
story.append(Paragraph("UPI Adoption vs. Fraud Risk: A Trend Analysis", title_style))
story.append(Paragraph(
    "Analyzing India's digital payments growth against fraud trends using official NPCI &amp; RBI data (FY2016-17 – FY2025-26)",
    subtitle_style))
story.append(HRFlowable(width="100%", thickness=1.2, color=TEAL, spaceAfter=8))

# --- KPI row ---
kpi_data = [
    [Paragraph("787.5B", kpi_num_style), Paragraph("Rs. 1,136L Cr", kpi_num_style),
     Paragraph("72.7%", kpi_num_style), Paragraph("6.6%", kpi_num_style)],
    [Paragraph("Total UPI transactions<br/>processed (2016–26)", kpi_label_style),
     Paragraph("Total transaction value<br/>processed (2016–26)", kpi_label_style),
     Paragraph("Decline in fraud ratio<br/>since FY18-19 peak", kpi_label_style),
     Paragraph("Forecast model error<br/>(MAPE, 6-month test)", kpi_label_style)],
]
kpi_table = Table(kpi_data, colWidths=[42*mm]*4)
kpi_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), LIGHTGREY),
    ('TOPPADDING', (0,0), (-1,0), 10),
    ('BOTTOMPADDING', (0,0), (-1,0), 2),
    ('BOTTOMPADDING', (0,1), (-1,1), 10),
    ('LINEAFTER', (0,0), (-2,-1), 0.75, colors.white),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(kpi_table)
story.append(Spacer(1, 10))

# --- Headline insight ---
story.append(Paragraph("Headline Finding", h2_style))
story.append(Paragraph(
    "UPI's Card/Internet fraud-to-transaction-value ratio peaked at 0.0086% in FY2018-19 and has declined "
    "~73% to 0.0024% by FY2024-25 — despite transaction value growing over 300x in the same period. "
    "This suggests RBI/NPCI security interventions have meaningfully outpaced the growth in fraud activity, "
    "even as digital payment adoption has scaled nationally.",
    headline_style))
story.append(Spacer(1, 8))

# --- Two column: Methodology | Key Findings ---
methodology = [
    Paragraph("<b>Data sources:</b> NPCI UPI Product Statistics (monthly volume/value, Apr 2016 – Aug 2026); "
              "RBI Report on Trend and Progress of Banking in India 2024-25, Appendix Table IV.7 (Card/Internet "
              "fraud, annual).", bullet_style),
    Paragraph("<b>Pipeline:</b> Python (pandas) for cleaning &amp; merging multi-source data &rarr; SQL "
              "(PostgreSQL, window functions) for YoY growth &amp; fraud-ratio aggregation &rarr; Power BI "
              "for the interactive dashboard.", bullet_style),
    Paragraph("<b>Forecasting:</b> Holt-Winters Exponential Smoothing (multiplicative trend + seasonality) on "
              "117 months of data, validated with a 6-month hold-out (MAPE 6.6%).", bullet_style),
    Paragraph("<b>Outlier detection:</b> Z-score method flagged FY2018-19 and FY2023-24 as statistically "
              "unusual years within UPI's mature era (chosen over ML given only 9 annual data points).",
              bullet_style),
]

findings = [
    Paragraph("Transaction value grew from Rs. 6,952 Cr (FY16-17) to over Rs. 26L Cr (FY24-25) — a "
              "structural shift in how India pays.", bullet_style),
    Paragraph("Fraud ratio's FY2023-24 spike is partly a reporting artifact: RBI reclassified 122 prior-year "
              "cases (Rs. 18,336 Cr) into FY2024-25 filings.", bullet_style),
    Paragraph("6-month forecast projects transaction value reaching ~Rs. 33.2L Cr by Feb 2027, continuing the "
              "current growth trajectory.", bullet_style),
    Paragraph("<b>Limitation:</b> RBI does not publicly release UPI-specific or state/channel-wise fraud data — "
              "Card/Internet category used as the closest official proxy.", bullet_style),
]

col_table = Table([[methodology, findings]], colWidths=[85*mm, 85*mm])
col_table.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (1,0), (1,0), 10),
]))

story.append(Paragraph("Methodology", h2_style))
story.append(Spacer(1, 2))

two_col_data = [[
    [Paragraph("<b>Data &amp; Tools</b>", body_style), Spacer(1,3)] + methodology,
    [Paragraph("<b>Key Findings</b>", body_style), Spacer(1,3)] + findings,
]]
two_col = Table(two_col_data, colWidths=[85*mm, 85*mm])
two_col.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (0,0), 0),
    ('LEFTPADDING', (1,0), (1,0), 10),
]))
story.append(two_col)

story.append(Spacer(1, 14))

# --- Tech stack tags ---
tech_style = ParagraphStyle('Tech', parent=styles['Normal'], fontSize=8.5, textColor=TEAL,
                             alignment=TA_CENTER, fontName='Helvetica-Bold', borderColor=TEAL,
                             borderWidth=0.75, borderPadding=5, backColor=colors.HexColor('#EAF6F7'))
tags = ["Python (pandas, statsmodels)", "SQL (PostgreSQL, window functions)",
        "Power BI (DAX)", "Holt-Winters Forecasting", "Statistical Outlier Detection"]
tag_row = Table([[Paragraph(t, tech_style) for t in tags]],
                 colWidths=[34*mm, 40*mm, 24*mm, 36*mm, 36*mm])
tag_row.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('LEFTPADDING', (0,0), (-1,-1), 2),
                              ('RIGHTPADDING', (0,0), (-1,-1), 2)]))
story.append(tag_row)
story.append(Spacer(1, 16))

story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#CCCCCC'), spaceAfter=6))

name_style = ParagraphStyle('Name', parent=styles['Normal'], fontSize=10, textColor=NAVY,
                             fontName='Helvetica-Bold')
story.append(Paragraph("[Your Name]  |  [your.email@example.com]  |  [LinkedIn URL]  |  [GitHub URL]", name_style))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "Built with Python, PostgreSQL, and Power BI. Full dashboard, SQL queries, and forecasting script "
    "available on GitHub. Data current as of the source publications' latest release (September 2026).",
    footnote_style))

doc.build(story)
print("PDF built: upi_project_summary.pdf")
