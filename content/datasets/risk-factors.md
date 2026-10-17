---
title: "Risk Factors"
type: "datasets"
summary: "Brazilian Fama-French and momentum risk factors (Rm-Rf, SMB, HML, WML, IML) and risk-free rate."
last_observation: "2026-09-08"
coverage_start: "2001-01-02"
frequency: "Daily"
description: "NEFIN computes a set of risk factors for the Brazilian stock market, following the Fama-French methodology adapted to the local market. Factors include the market premium (Rm-Rf), size (SMB), value (HML), momentum (WML), and illiquidity (IML), as well as the risk-free rate."
dashboard: true
dashboard_csv: "/nefindata/risk-factors/nefin_factors.csv"
dashboard_versions:
  - label: "Value weighted"
    csv: "/nefindata/risk-factors/nefin_factors.csv"
  - label: "Equally weighted"
    csv: "/nefindata/risk-factors/nefin_factors_equally_weighted.csv"
downloads:
  - label: "NEFIN Risk Factors, value weighted (CSV)"
    url: "/nefindata/risk-factors/nefin_factors.csv"
  - label: "NEFIN Risk Factors, equally weighted (CSV)"
    url: "/nefindata/risk-factors/nefin_factors_equally_weighted.csv"
  - label: "NEFIN Risk Factors, value weighted, monthly (CSV)"
    url: "/nefindata/risk-factors/nefin_factors_monthly.csv"
  - label: "NEFIN Risk Factors, equally weighted, monthly (CSV)"
    url: "/nefindata/risk-factors/nefin_factors_equally_weighted_monthly.csv"
  - label: "Methodology (PDF)"
    url: "/nefindata/methodology/nefin_methodology.pdf"
table:
  headers: ["Risk Factor", "6 months", "1 year", "5 years", "Full sample"]
  rows:
    - ["Rm-Rf",     "-7.05%",  "10.87%",  "-3.19%",  "1.26%"]
    - ["SMB",       "-19.10%", "-19.20%", "-11.14%", "-2.17%"]
    - ["HML",       "-6.41%",  "1.94%",   "22.43%",  "3.51%"]
    - ["WML",       "-10.03%", "-12.91%", "12.21%",  "8.75%"]
    - ["IML",       "-18.48%", "-25.25%", "-10.24%", "-1.49%"]
    - ["Risk-Free", "14.34%",  "14.44%",  "12.53%",  "11.87%"]
table_caption: "Annualized returns of the value-weighted factors, sample ending 8 September 2026. The summary table is a periodic snapshot; the CSV and the chart below carry the full series up to the last observation."
tables:
  - caption: "Annualized returns of the equally weighted factors, sample ending 8 September 2026. Rm-Rf and the risk-free rate are the same as above."
    headers: ["Risk Factor", "6 months", "1 year", "5 years", "Full sample"]
    rows:
      - ["SMB", "-25.87%", "-21.54%", "-8.80%",  "-3.16%"]
      - ["HML", "-7.62%",  "-2.81%",  "12.21%",  "6.61%"]
      - ["WML", "14.14%",  "11.12%",  "13.81%",  "14.62%"]
      - ["IML", "-21.31%", "-18.12%", "-5.00%",  "-0.22%"]
aliases:
  - "/data/risk_factors.html"
---

The factors come in two versions, with the same columns and dates. SMB, HML, WML and IML
are the difference between the returns of the first and third tercile portfolios,
weighted either by **market value** (`nefin_factors.csv`) or **equally**
(`nefin_factors_equally_weighted.csv`). The market factor and the risk-free rate are the
same in both. The two versions differ substantially (daily correlation between 0.63 and
0.85), so state which one you use. The tables below summarize each version, and the
chart switches between them.

Both versions are also published at **monthly** frequency (`…_monthly.csv`, dated by
year and month, complete months only). As in the Fama-French data library, each monthly
factor is the spread between the monthly returns of the two portfolios, not the
compounded daily factor, so the two differ slightly. All returns are fractions
(0.01 = 1%).
