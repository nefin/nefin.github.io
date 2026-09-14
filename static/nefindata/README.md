# NEFIN data — file naming policy

This describes the fixed URL scheme for every downloadable data file on
[nefin.com.br](https://nefin.com.br), so that scripts and libraries (e.g. a
Python `nefindata` package) can build download URLs programmatically instead
of scraping the site.

## URL pattern

```
https://nefin.com.br/nefindata/{datafolder}/{filename}.{filenametype}
```

- **`{datafolder}`** is always the dataset's slug — the same string used in
  its page URL (`nefin.com.br/data/{datafolder}/`) and in its
  `content/datasets/{datafolder}.md` source file. Written in **kebab-case**
  (lowercase, words separated by `-`), e.g. `risk-factors`, `cost-of-equity`.
- **`{filename}`** identifies one file inside that dataset. Written in
  **lowercase snake_case** (lowercase, words separated by `_`, no spaces, no
  hyphens). Hyphens are reserved for the `{datafolder}` level, so a filename
  never contains one — this lets a parser split `datafolder` from `filename`
  on the first `-` vs `_` unambiguously.
- **`{filenametype}`** is the file extension, always lowercase (`csv`, `xls`,
  `pdf`, `zip`).

There is one shared folder, `methodology/`, holding the single PDF
(`nefin_methodology.pdf`) referenced by every dataset page — it isn't tied to
one dataset, so it doesn't follow the per-dataset key.

**These URLs are a public API.** They get pasted into papers, notebooks and
`pandas.read_csv()` calls outside this repo. Renaming or moving a file under
`static/nefindata/` breaks it for everyone who already has the old link —
treat it as a breaking change, not a refactor, and update the matching
`downloads[].url` (and `dashboard_csv` for risk-factors) in the dataset's
front matter in the same change. See `CLAUDE.md` → *Data file URLs* for the
maintenance-side rules.

## Current files, by dataset

| `{datafolder}` | Files | Format(s) |
|---|---|---|
| `cost-of-equity` | `basic_products`, `construction`, `consumer`, `energy`, `finance`, `manufacturing`, `other` | csv + xls |
| `dividend-yield` | `dividend_yield` | csv + xls |
| `loan-fees` | `loan_fees` | csv + xls |
| `portfolios` | `3_portfolios_sorted_by_size`, `3_portfolios_sorted_by_book_to_market`, `3_portfolios_sorted_by_momentum`, `3_portfolios_sorted_by_illiquidity`, `4_portfolios_sorted_by_size_and_book_to_market_2x2`, `4_portfolios_sorted_by_size_and_illiquidity_2x2`, `4_portfolios_sorted_by_size_and_momentum_2x2`, `7_portfolios_sorted_by_industry` | xls only |
| `risk-factors` | `nefin_factors` | csv |
| `short-interest` | `average_short_interest`, `average_days_to_cover`, `average_loan_fee` | csv |
| `spot-rate-curve` | `spot_rate_curve` | csv + xls |
| `volatility-index` | `ivol_br`, `risk_aversion`, `variance_premium` | csv (ivol_br only) + xls |
| `methodology` | `nefin_methodology` | pdf |

Example: NEFIN's risk factors CSV is always at
`https://nefin.com.br/nefindata/risk-factors/nefin_factors.csv`.

> `risk-factors/` also carries `portfolio_3x3.zip` and five
> `portfolio_by_*.csv` files that no dataset page currently links to (found
> unreferenced during the 2026-09 cleanup, kept rather than deleted since
> they're live data, not legacy cruft). Don't assume they're stable/supported
> until a dataset page documents them — check `content/datasets/risk-factors.md`
> for what's actually promised.

## For a Python client

Since there are only a handful of datasets, hardcoding the table above as a
small registry (`{dataset_key: {file_key: extension}}`) inside the library is
the simplest approach — no need to scrape the site or maintain a separate
generated manifest. Prefer the `.csv` file when one exists (all these `.xls`
files are the legacy format kept for people who want it directly in Excel;
`.csv` is smaller and doesn't need `xlrd`). `portfolios` is the one dataset
with `.xls` only.

If this table and `content/datasets/*.md`'s `downloads` fields ever disagree,
the front matter in `content/datasets/*.md` is authoritative — it's what's
actually rendered on each dataset's download page.
