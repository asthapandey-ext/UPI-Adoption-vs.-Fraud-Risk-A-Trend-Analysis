UPI Adoption vs. Fraud Risk: A Trend Analysis

A data analysis project examining the relationship between India's UPI (Unified Payments Interface) transaction growth and digital payment fraud trends, using official government data from NPCI and RBI — with a forward-looking forecasting model built on top.

📄 One-page project summary: upi_project_summary.pdf

🔑 Headline Finding

UPI's Card/Internet fraud-to-transaction-value ratio peaked at 0.0086% in FY2018-19 and has declined ~73% to 0.0024% by FY2024-25 — despite transaction value growing over 300x in the same period. This suggests RBI/NPCI security interventions have meaningfully outpaced the growth in fraud activity.

📊 Dashboard

The Power BI dashboard has 3 pages:

Fraud Risk — annual fraud-to-transaction-value ratio trend (FY2016-17 to FY2024-25), KPI cards, and statistical outlier flags
Adoption Trend — monthly UPI transaction volume/value growth (April 2016 – August 2026)
Forecasting — 6-month forward forecast of UPI transaction value

(Add dashboard screenshots here — e.g. ![Fraud Risk Page](screenshots/fraud_risk.png))

🗂️ Data Sources
Source	What it provides	Granularity
NPCI UPI Product Statistics	Monthly UPI transaction volume & value	Monthly, Apr 2016 – Aug 2026
RBI Report on Trend and Progress of Banking in India 2024-25, Appendix Table IV.7	Card/Internet category fraud (count & amount)	Annual (fiscal year), FY2004-05 – FY2025-26

Note on scope: RBI does not publicly release UPI-specific or state/channel-wise fraud data. The "Card/Internet" fraud category — which includes UPI along with other card and internet-banking fraud — is used as the closest available official proxy. This limitation is disclosed on the dashboard itself.

🛠️ Tech Stack & Pipeline
Raw data (NPCI + RBI)
        │
        ▼
Python (pandas) — cleaning, merging multi-source monthly/annual data
        │
        ▼
PostgreSQL — SQL aggregation using window functions (LAG, RANK) for
             YoY growth and fraud-ratio calculations
        │
        ▼
Power BI — interactive 3-page dashboard with DAX measures
        │
        ▼
Python (statsmodels) — Holt-Winters forecasting + z-score outlier flagging
Python: pandas, numpy, statsmodels, scikit-learn
SQL: PostgreSQL, window functions (LAG, RANK)
BI: Power BI (DAX measures, custom KPI cards)
Forecasting: Holt-Winters Exponential Smoothing (multiplicative trend + seasonality)
📁 Repository Structure
├── data/
│   ├── upi_monthly_master_2016_2026.csv      # Cleaned monthly UPI volume/value
│   ├── upi_fraud_ratio_FINAL.csv             # Annual fraud ratio (RBI Card/Internet)
│   └── fraud_ratio_outlier_flags.csv         # Z-score outlier flags by FY
├── sql/
│   └── upi_analysis_queries_postgres.sql     # Aggregation queries (YoY growth, ratio, ranking)
├── scripts/
│   ├── upi_forecast_model.py                 # Holt-Winters forecasting model
│   └── fraud_outlier_flagging.py             # Statistical outlier detection
├── upi_project_summary.pdf                   # 1-page recruiter-facing summary
└── README.md
🔮 Forecasting Model

Method: Holt-Winters Exponential Smoothing (multiplicative trend + seasonality)

Why not a more complex model (e.g. LSTM)? Only 117 monthly observations are available — a data volume where simpler, well-understood models generalize more reliably than models that need far more data to avoid overfitting.

Validation: Last 6 months held out as a test set.

RMSE: ₹203,047 crore
MAPE: 6.6%

Forecast: UPI transaction value projected to grow from ~₹29.8L Cr (Aug 2026) to ~₹33.2L Cr (Feb 2027).

Run it yourself:

bash
pip install pandas numpy statsmodels scikit-learn
python scripts/upi_forecast_model.py
📈 Statistical Outlier Detection

With only 7-9 annual fraud-ratio data points, a full ML anomaly-detection model would overfit. Instead, a z-score method (mean ± std. dev. across the mature-era years) flags statistically unusual years:

FY	Fraud Ratio	Z-score	Flag
2018-19	0.00863%	1.49	Outlier
2023-24	0.00729%	1.01	Outlier
Others	—	|z| < 1	Normal

Run it yourself:

bash
python scripts/fraud_outlier_flagging.py
⚠️ Limitations
No UPI-specific fraud data: RBI's Card/Internet category is a proxy, not a UPI-only figure.
No state/channel-level fraud breakdown: Not publicly available; the geo/channel dimension originally scoped for this project was dropped for this reason.
Small annual sample (9 points): Outlier flagging uses a transparent statistical method rather than ML, by design.
Minor data gaps: A few months (e.g. Apr–May of some fiscal years) are missing from NPCI's public monthly releases.
👤 Author

[Astha Pandey] [asthapandeylinkdin@gmail.com] · [https://www.linkedin.com/in/astha-pandey-821a603a0/] · [Portfolio URL]
