---
title: "Loan Fees"
type: "datasets"
summary: "Weekly securities lending fee (loan fee) for Brazilian equities in the BTC market."
description: "Weekly average securities lending fee (aluguel de ações) for Brazilian equities traded in the BTC market, expressed as a fraction per year (0.015 = 1.5%). Each observation is the average of the daily loan fee over the week, dated on its last trading day."
last_observation: "2026-09-08"
coverage_start: "2013-01-04"
frequency: "Weekly"
downloads:
  - label: "Loan Fees (CSV)"
    url: "/nefindata/loan-fees/loan_fees.csv"
  - label: "Loan Fees (XLS)"
    url: "/nefindata/loan-fees/loan_fees.xls"
  - label: "Methodology (PDF)"
    url: "/nefindata/methodology/nefin_methodology.pdf"
aliases:
  - "/data/loan_fees.html"
---

This is the weekly version of the daily average loan fee published on the
[Short Interest](/data/short-interest/) page (in percent per year there, as a fraction
here). The series was discontinued in September 2023 and resumed in October 2026, rebuilt
from the daily data for the whole period since 2013. The rebuilt history moves with the
version published until 2023 (correlation 0.82) but sits about 16% higher, so
re-download the file rather than appending to an old copy.

The few weeks above 5% in 2013–2014 are real, not data errors: they are loans of VALE5
and PETR4 taken around interest-on-equity (JCP) record dates, settled three sessions
later.
