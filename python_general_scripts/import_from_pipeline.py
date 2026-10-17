#!/usr/bin/env python3
"""Refresh static/nefindata/ from the nefin-portfolio pipeline output.

    python3 python_general_scripts/import_from_pipeline.py /path/to/nefin-portfolio/data
    python3 python_general_scripts/update_dataset_dates.py      # then refresh the page dates

Reads 05_model_input/ (factors, 3x3 portfolio CSVs), 08_reporting/ (multi-sheet
portfolio workbooks) and 06_models/ (dividend yield, illiquidity, short interest + weekly loan fee, cost of equity)
and rewrites the published files *in their existing public layout* (column names,
sheet names and order, file names), since those are a public API — see
static/nefindata/README.md. The pipeline starts some series in 2000; the published
factor and portfolio files keep their historical 2001-01-02 start.

Not covered: spot-rate-curve, volatility-index (discontinued archives).
Units the site states in prose (content/datasets/short-interest.md): short interest
in per mille, days-to-cover in days, loan fee in % per year.

Requires: pandas, openpyxl, xlwt (pandas 2 can no longer write .xls itself).
The risk-factors summary table in content/datasets/risk-factors.md is *not*
recomputed here: annualized compound return over calendar days (365.25) for the
last 6m / 1y / 5y and the full sample.
"""
import io, sys, zipfile
from pathlib import Path
import pandas as pd

if len(sys.argv) != 2:
    sys.exit(__doc__)
SRC = Path(sys.argv[1])
DST = Path(__file__).resolve().parent.parent / "static" / "nefindata"
MI, REP, MOD = SRC / "05_model_input", SRC / "08_reporting", SRC / "06_models"
START = "2001-01-02"  # first date of the published factor and portfolio series
log = []

def write_xls(path, sheets):
    """pandas 2 dropped the xlwt engine; write legacy .xls directly."""
    import math, xlwt
    INT_COLS = {"year", "month", "day", "ano", "mes", "dia", "Industry Code"}
    wb = xlwt.Workbook()
    for name, df in sheets:
        ws = wb.add_sheet(name)
        for c, col in enumerate(df.columns):
            ws.write(0, c, str(col))
        for r, row in enumerate(df.itertuples(index=False), 1):
            for c, v in enumerate(row):
                if v is None or (isinstance(v, float) and math.isnan(v)):
                    continue
                ws.write(r, c, v if isinstance(v, str) else int(v) if df.columns[c] in INT_COLS else float(v))
    wb.save(str(path))

# ---------- A1. risk factors: same layout as the published R-style CSV ----------
# Two versions: SMB/HML/WML/IML from value-weighted tercile returns (nefin_factors.csv,
# the series published since the start) and from equal-weighted ones, as methodology
# section 5 describes. The market factor and the risk-free rate are the same in both.
for src, out in [("factors", "nefin_factors"), ("factors_equally_weighted", "nefin_factors_equally_weighted")]:
    f = pd.read_csv(MI / f"{src}.csv", index_col=0, parse_dates=["date"]).set_index("date")
    f = f.rename(columns={"mkt-rf": "Rm_minus_Rf", "smb": "SMB", "hml": "HML",
                          "mom": "WML", "illiq": "IML", "rf": "Risk_Free"})
    f = f.loc[START:, ["Rm_minus_Rf", "SMB", "HML", "WML", "IML", "Risk_Free"]]
    assert not f.isna().any().any()
    buf = io.StringIO()
    buf.write('"","Date","Rm_minus_Rf","SMB","HML","WML","IML","Risk_Free"\n')
    for i, (d, r) in enumerate(f.iterrows(), 1):
        buf.write(f'"{i}",{d:%Y-%m-%d},' + ",".join(repr(float(v)) for v in r) + "\n")
    (DST / f"risk-factors/{out}.csv").write_text(buf.getvalue())
    log.append(f"{out}.csv {f.index.min().date()}..{f.index.max().date()} rows={len(f)}")

# Monthly factors (complete months only; each factor is the spread of monthly
# portfolio returns, not the compounded daily factor). Same column names as the daily
# files, dated by year and month, from the same 2001 start.
for src, out in [("nefin_factors_monthly", "nefin_factors_monthly"),
                 ("nefin_factors_equally_weighted_monthly", "nefin_factors_equally_weighted_monthly")]:
    m = pd.read_csv(MI / f"{src}.csv")
    m = m.rename(columns={"mkt-rf": "Rm_minus_Rf", "smb": "SMB", "hml": "HML",
                          "mom": "WML", "illiq": "IML", "rf": "Risk_Free"})
    m = m[m.year * 100 + m.month >= int(START[:4]) * 100 + int(START[5:7])]
    m = m[["year", "month", "Rm_minus_Rf", "SMB", "HML", "WML", "IML", "Risk_Free"]]
    assert not m.isna().any().any()
    m.to_csv(DST / f"risk-factors/{out}.csv", index=False)
    log.append(f"{out}.csv {m.year.iloc[0]}-{m.month.iloc[0]:02d}..{m.year.iloc[-1]}-{m.month.iloc[-1]:02d} rows={len(m)}")

# ---------- A2. 3x3 portfolio CSVs + zip ----------
csvs = {}
for out, src in [("portfolio_by_size", "portfolio_by_size_3x3"), ("portfolio_by_book_to_market", "portfolio_by_bm_3x3"),
                 ("portfolio_by_illiq", "portfolio_by_illiq_3x3"), ("portfolio_by_momentum", "portfolio_by_mom_3x3")]:
    d = pd.read_csv(MI / f"{src}.csv")
    assert list(d.columns) == ["date", "low", "medium", "high"]
    d = d[d.date >= START]
    csvs[out] = d.to_csv(index=False)
ind = pd.read_csv(MI / "industry_portfolio.csv")
long = ind.melt(id_vars="date", var_name="setor_novo", value_name="rent_pond").dropna()
long = long.sort_values(["setor_novo", "date"])[["setor_novo", "date", "rent_pond"]]
csvs["portfolio_by_industry"] = long.to_csv(index=False)
for name, text in csvs.items():
    (DST / f"risk-factors/{name}.csv").write_text(text)
    log.append(f"{name}.csv last={text.strip().splitlines()[-1].split(',')[1 if name=='portfolio_by_industry' else 0]}")
with zipfile.ZipFile(DST / "risk-factors/portfolio_3x3.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for name in sorted(csvs):
        # Fixed timestamp: identical data -> byte-identical zip, so git sees no churn.
        z.writestr(zipfile.ZipInfo(f"{name}.csv", date_time=(2000, 1, 1, 0, 0, 0)), csvs[name],
                   compress_type=zipfile.ZIP_DEFLATED)

# ---------- B1. portfolios .xls (multi-sheet, legacy column + sheet names) ----------
# Returns are daily (year, month, day); stock counts and market values monthly
# (year, month); book values and book-to-market annual (year), as in the methodology
# (section 2) and the files published until 2023.
# The published file itself is the template: its sheet order and per-sheet column
# names are kept (they are inconsistent across sheets, e.g. Size1_Mom1 for returns
# but S1_Mom1 for stock counts), and sheets the pipeline doesn't produce (the
# 2001-2014 "Number of firms", "Market Value", ... in some files) are copied as-is.
SHEETS = {"Equally Weighted Returns": ("Equally Weighted Returns", ["year", "month", "day"]),
          "Value Weighted Returns": ("Value Weighted Returns", ["year", "month", "day"]),
          "Number of stocks": ("Number of Stocks", ["year", "month"]),
          "Average market value": ("Average Market Value", ["year", "month"]),
          "Average book value": ("Average Book Value", ["year"]),
          "Average book-to-market ratio": ("Average Book-to-Market", ["year"])}
def one_way(p): return {"low": f"{p}1", "medium": f"{p}2", "high": f"{p}3"}
def two_way(k, p): return {f"size_low_{k}_low": f"Size1_{p}1", f"size_low_{k}_high": f"Size1_{p}2",
                           f"size_high_{k}_low": f"Size2_{p}1", f"size_high_{k}_high": f"Size2_{p}2"}
INDUSTRIES = ["Basic Products", "Construction", "Consumer", "Energy", "Finance", "Manufacturing", "Other"]
XLS = [("3_portfolios_sorted_by_size", "size_portfolio", one_way("Size")),
       ("3_portfolios_sorted_by_book_to_market", "bm_portfolio", one_way("BM")),
       ("3_portfolios_sorted_by_momentum", "mom_portfolio", one_way("Mom")),
       ("3_portfolios_sorted_by_illiquidity", "illiq_portfolio", one_way("ILLIQ")),
       ("4_portfolios_sorted_by_size_and_book_to_market_2x2", "size_bm_portfolio", two_way("bm", "BM")),
       ("4_portfolios_sorted_by_size_and_illiquidity_2x2", "size_illiq_portfolio", two_way("illiq", "ILLIQ")),
       ("4_portfolios_sorted_by_size_and_momentum_2x2", "size_mm_portfolio", two_way("mm", "Mom")),
       ("7_portfolios_sorted_by_industry", "industry_portfolio",
        {name: f"Industry_{k}" for k, name in enumerate(INDUSTRIES, 1)})]
start = pd.Timestamp(START)
for out, src, ren in XLS:
    path = DST / f"portfolios/{out}.xls"
    template = pd.read_excel(path, sheet_name=None)
    book = pd.read_excel(REP / f"{src}.xlsx", sheet_name=None)
    sheets = []
    for name, tpl in template.items():
        if name not in SHEETS:
            sheets.append((name, tpl))
            continue
        new_name, keys = SHEETS[name]
        target = [c for c in tpl.columns if c not in keys]
        if new_name.endswith("Returns"):
            assert target == list(ren.values()), (out, name, target)  # positional mapping holds
        d = book[new_name]
        assert set(ren) <= set(d.columns) and set(keys) <= set(d.columns), (src, new_name, d.columns)
        d = d[[*keys, *ren]].set_axis([*keys, *target], axis=1)
        d[keys] = d[keys].astype(int)
        d = d[d.year * 10000 + d.get("month", 12) * 100 + d.get("day", 31)
              >= start.year * 10000 + start.month * 100 + start.day]
        sheets.append((name, d))
    write_xls(path, sheets)
    last = book["Value Weighted Returns"].iloc[-1]
    log.append(f"{out}.xls last={int(last.year)}-{int(last.month):02d}-{int(last.day):02d}")

# ---------- B2. dividend yield: weekly (last trading day of each week) ----------
dy = pd.read_csv(MOD / "div_yield_index.csv", parse_dates=["date"]).set_index("date").dividend_yield
wk = dy.groupby(dy.index.to_period("W-FRI")).tail(1).loc["2001-02-02":]
out = pd.DataFrame({"year": wk.index.year, "month": wk.index.month, "day": wk.index.day, "yield_week_pc": wk.values})
out.rename(columns={"year": "ano", "month": "mes", "day": "dia"}).to_csv(DST / "dividend-yield/dividend_yield.csv", index=False)
write_xls(DST / "dividend-yield/dividend_yield.xls", [("Sheet1", out)])
log.append(f"dividend_yield {wk.index.min().date()}..{wk.index.max().date()} weeks={len(wk)}")

# ---------- B3. illiquidity index (new file) ----------
il = pd.read_csv(MOD / "illiq_index.csv", parse_dates=["date"])
il = il[il.date >= "2000-02-01"][["date", "illiquidity"]]
(DST / "illiquidity-index").mkdir(exist_ok=True)
il.to_csv(DST / "illiquidity-index/illiquidity_index.csv", index=False, date_format="%Y-%m-%d")
log.append(f"illiquidity_index {il.date.min().date()}..{il.date.max().date()} months={len(il)}")

# ---------- C. short interest: same files, same columns ----------
for name in ["average_short_interest", "average_days_to_cover", "average_loan_fee"]:
    d = pd.read_csv(MOD / f"{name}.csv")
    assert list(d.columns) == ["date", name] and not d[name].isna().any()
    d.to_csv(DST / f"short-interest/{name}.csv", index=False)
    log.append(f"{name} {d.date.iloc[0]}..{d.date.iloc[-1]} rows={len(d)}")

# ---------- C2. weekly loan fee (methodology 10.3): mean of the daily series ----------
# Dated on the week's last trading day, as a fraction per year (the daily file is in %).
lf = pd.read_csv(MOD / "average_loan_fee.csv", parse_dates=["date"]).set_index("date").average_loan_fee / 100
wk = lf.groupby(lf.index.to_period("W-FRI"))
wk = pd.DataFrame({"date": wk.apply(lambda x: x.index[-1]), "fee": wk.mean()})
out = pd.DataFrame({"year": wk.date.dt.year, "month": wk.date.dt.month, "day": wk.date.dt.day, "fee": wk.fee})
csv = out.rename(columns={"year": "ano", "month": "mes", "day": "dia", "fee": "semana_aluguel_100"})
csv.to_csv(DST / "loan-fees/loan_fees.csv", index=False, float_format="%.7g")
write_xls(DST / "loan-fees/loan_fees.xls", [("Sheet1", out.rename(columns={"fee": "week_loan_fee"}))])
log.append(f"loan_fees {wk.date.iloc[0].date()}..{wk.date.iloc[-1].date()} weeks={len(wk)}")

# ---------- D. cost of equity: one file per sector, csv (;) + xls ----------
COE_XLS = ["Month/Year", "1-Year Project", "5-Year Project", "10-Year Project", "20-Year Project"]
def num(v):  # published style: 2 decimals, no trailing ".0", empty when missing
    return "" if pd.isna(v) else str(int(v)) if float(v).is_integer() else repr(round(float(v), 2))
for src in sorted((MOD / "cost_of_equity").glob("*.csv")):
    d = pd.read_csv(src, sep=";")
    assert list(d.columns) == ["data_mes_ano", "custo_capital_1ano_1", "custo_capital_5anos_1",
                               "custo_capital_10anos_1", "custo_capital_20anos_1"], d.columns
    text = ";".join(d.columns) + "\n" + "".join(
        f'"{r[0]}";' + ";".join(num(v) for v in r[1:]) + "\n" for r in d.itertuples(index=False))
    (DST / f"cost-of-equity/{src.name}").write_text(text)
    write_xls(DST / f"cost-of-equity/{src.stem}.xls", [("Sheet1", d.set_axis(COE_XLS, axis=1))])
    log.append(f"cost_of_equity/{src.stem} {d.iloc[0, 0]}..{d.iloc[-1, 0]} rows={len(d)}")

print("\n".join(log))
