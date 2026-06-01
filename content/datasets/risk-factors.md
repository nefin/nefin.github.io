---
title: "Risk Factors"
type: "datasets"
summary: "Brazilian Fama-French and momentum risk factors (Rm-Rf, SMB, HML, WML, IML) and risk-free rate."
description: "NEFIN computes a set of risk factors for the Brazilian stock market, following the Fama-French methodology adapted to the local market. Factors include the market premium (Rm-Rf), size (SMB), value (HML), momentum (WML), and illiquidity (IML), as well as the risk-free rate."
updated: "January 2026"
dashboard: true
dashboard_csv: "/resources/risk_factors/nefin_factors.csv"
downloads:
  - label: "NEFIN Risk Factors (CSV)"
    url: "/resources/risk_factors/nefin_factors.csv"
  - label: "Methodology (PDF)"
    url: "/resources/NEFIN_methodology.pdf"
table:
  headers: ["Risk Factor", "6 months", "1 year", "5 years", "Full sample"]
  rows:
    - ["Rm-Rf", "53.34%", "14.93%", "-2.79%", "1.33%"]
    - ["SMB",   "1.29%",  "25.39%", "7.19%",  "-1.69%"]
    - ["HML",   "8.55%",  "13.22%", "18.39%", "6.80%"]
    - ["WML",   "10.05%", "-0.26%", "16.39%", "14.60%"]
    - ["IML",   "-13.85%","-6.58%", "0.72%",  "0.42%"]
    - ["Risk-Free","14.90%","14.44%","11.22%","11.81%"]
table_caption: "Annualized returns up to 01.30.2026"
---
