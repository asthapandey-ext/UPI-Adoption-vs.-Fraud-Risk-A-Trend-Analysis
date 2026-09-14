"""
Fraud Ratio Outlier Flagging (Statistical Method)
====================================================
Project: UPI Adoption vs Fraud Risk Trend Analysis

Purpose:
    Flag financial years where the Card/Internet fraud-to-transaction-value
    ratio was statistically unusual, using a z-score against the mean and
    standard deviation of the "mature era" (post-launch) years.

Why a statistical method, not a machine learning model:
    Only 7-9 annual data points are available here (one per fiscal year).
    This is far too small a sample to train or validate an ML model
    reliably — any model would essentially memorize the data rather than
    learn a generalizable pattern. A z-score is the right-sized tool for
    this data volume: transparent, statistically defensible, and easy to
    explain to a non-technical stakeholder.

Note on scope:
    FY2016-17 and FY2017-18 (UPI's launch years) are excluded from this
    calculation. Their fraud ratios were extreme outliers themselves
    (0.60% and 0.09%) purely because transaction volume was still tiny —
    including them would swamp the z-scores of every other year and make
    the comparison meaningless.
"""

import numpy as np
import csv

data = {
    '2018-19': 0.00863,
    '2019-20': 0.00605,
    '2020-21': 0.00290,
    '2021-22': 0.00184,
    '2022-23': 0.00199,
    '2023-24': 0.00729,
    '2024-25': 0.00236,
}

values = np.array(list(data.values()))
mean = values.mean()
std = values.std(ddof=1)

Z_THRESHOLD = 1.0

print(f"Mean fraud ratio (mature era): {mean:.5f}%")
print(f"Std deviation: {std:.5f}%\n")
print(f"{'FY':<10}{'Ratio (%)':>12}{'Z-score':>10}{'Flag':>15}")

results = []
for fy, v in data.items():
    z = (v - mean) / std
    flag = "Outlier" if abs(z) > Z_THRESHOLD else "Normal"
    print(f"{fy:<10}{v:>12.5f}{z:>10.2f}{flag:>15}")
    results.append({'FY': fy, 'fraud_ratio_pct': v, 'z_score': round(z, 2), 'flag': flag})

with open('fraud_ratio_outlier_flags.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['FY', 'fraud_ratio_pct', 'z_score', 'flag'])
    w.writeheader()
    w.writerows(results)

print("\nSaved: fraud_ratio_outlier_flags.csv")
print("\nInterpretation:")
print("  FY2018-19 and FY2023-24 stand out as statistically unusual years")
print("  within the mature era — both are worth a one-line note on the")
print("  dashboard, but neither invalidates the overall declining trend.")