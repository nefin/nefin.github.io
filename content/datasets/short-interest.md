---
title: Short Interest
type: datasets
summary: Daily short interest, days-to-cover and loan fee for the Brazilian stock loan market.
last_observation: "2026-09-08"
coverage_start: "2012-11-07"
frequency: "Daily"
description: "NEFIN computes three daily statistics for the Brazilian stock loan
  market: the short interest (shares on loan over shares outstanding), the
  days-to-cover (shares on loan over the average daily number of shares traded
  in the previous 30 sessions) and the loan fee. Each is averaged across
  eligible stocks, weighted by the value of open loan positions."
downloads:
  - label: Average Short Interest (CSV)
    url: /nefindata/short-interest/average_short_interest.csv
  - label: Average Days-to-Cover (CSV)
    url: /nefindata/short-interest/average_days_to_cover.csv
  - label: Average Loan Fee (CSV)
    url: /nefindata/short-interest/average_loan_fee.csv
  - label: Methodology (PDF)
    url: /nefindata/methodology/nefin_methodology.pdf
aliases:
  - "/data/short_interest.html"
---

**Days-to-cover is in days since the October 2026 update.** Earlier versions of this
file used a different volume measure in the denominator, which put the series around 0.4;
the current series follows the methodology and sits around 7 days.
The whole history was recomputed, so re-download the file rather than appending to an old copy.
Short interest is in per mille of shares outstanding (32 = 3.2%), and the loan fee in percent
per year; both are now computed over eligible stocks only, as in the methodology.
A weekly version of the loan fee, as a fraction, is on the [Loan Fees](/data/loan-fees/) page.
