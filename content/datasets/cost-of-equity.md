---
title: "Cost of Equity"
type: "datasets"
summary: "Monthly cost of equity for seven Brazilian sectors, at 1-, 5-, 10- and 20-year horizons."
description: "Estimated cost of equity for Brazilian listed firms, reported separately for seven sectors (Basic Products, Construction, Consumer, Energy, Finance, Manufacturing and Other). Each file gives the monthly discount rate, in percent per year, for project horizons of 1, 5, 10 and 20 years: a real risk-free rate plus the sector's CAPM beta times the US market risk premium. See the methodology PDF for the estimation procedure."
last_observation: "2026-09-01"
coverage_start: "2005-01-01"
frequency: "Monthly"
downloads:
  - label: "Basic Products (CSV)"
    url: "/nefindata/cost-of-equity/basic_products.csv"
  - label: "Basic Products (XLS)"
    url: "/nefindata/cost-of-equity/basic_products.xls"
  - label: "Construction (CSV)"
    url: "/nefindata/cost-of-equity/construction.csv"
  - label: "Construction (XLS)"
    url: "/nefindata/cost-of-equity/construction.xls"
  - label: "Consumer (CSV)"
    url: "/nefindata/cost-of-equity/consumer.csv"
  - label: "Consumer (XLS)"
    url: "/nefindata/cost-of-equity/consumer.xls"
  - label: "Energy (CSV)"
    url: "/nefindata/cost-of-equity/energy.csv"
  - label: "Energy (XLS)"
    url: "/nefindata/cost-of-equity/energy.xls"
  - label: "Finance (CSV)"
    url: "/nefindata/cost-of-equity/finance.csv"
  - label: "Finance (XLS)"
    url: "/nefindata/cost-of-equity/finance.xls"
  - label: "Manufacturing (CSV)"
    url: "/nefindata/cost-of-equity/manufacturing.csv"
  - label: "Manufacturing (XLS)"
    url: "/nefindata/cost-of-equity/manufacturing.xls"
  - label: "Other (CSV)"
    url: "/nefindata/cost-of-equity/other.csv"
  - label: "Other (XLS)"
    url: "/nefindata/cost-of-equity/other.xls"
  - label: "Methodology (PDF)"
    url: "/nefindata/methodology/nefin_methodology.pdf"
aliases:
  - "/data/cost_of_equity.html"
---

The whole history was recomputed in October 2026. Until then the seven sector files
published the same series, so the new values differ from the old ones by 1 to 10
percentage points: the beta is now estimated for each sector (between 0.80 and 1.64),
and the US market risk premium is the excess return of stocks over T-bills from the
Fama-French data library. The real risk-free rate is unchanged. Construction starts in
February 2009, since no construction company was eligible before 2007 and the beta needs
24 months of returns. The 1-year real rate uses the one-year LTN instead of the 360-day
DI swap named in the methodology, which the Central Bank stopped publishing in 2019.
