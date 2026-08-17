#!/usr/bin/env python3
"""Refresh `coverage_start` / `last_observation` in content/datasets/*.md.

The website's freshness badge ("Updated Jul 2026" / "Last observation May 2020")
is computed from these two fields. They must describe the data, not the day
someone edited the page — so this script reads the actual files and writes the
dates back into the front matter.

Run it after every data update:

    python3 python_general_scripts/update_dataset_dates.py          # apply
    python3 python_general_scripts/update_dataset_dates.py --check  # CI: fail if stale

Requires: pandas, xlrd (for the legacy .xls files).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "datasets"
STATIC = ROOT / "static"

# Which file backs each dataset page, and how to find the date in it.
#   date="iso"    -> a column holding YYYY-MM-DD
#   date="ymd"    -> separate year / month / day columns
#   date="myyyy"  -> a "M/YYYY" string column
SOURCES: dict[str, dict] = {
    "risk-factors":      {"file": "resources/risk_factors/nefin_factors.csv",        "date": "iso",   "col": "Date"},
    "short-interest":    {"file": "resources/stock_loans/average_short_interest.csv", "date": "iso",   "col": "date"},
    "spot-rate-curve":   {"file": "resources/spot_rate_curve/spot_rate_curve.csv",   "date": "iso",   "col": "Date"},
    "volatility-index":  {"file": "resources/volatility_index/IVol-BR.csv",          "date": "ymd"},
    "dividend-yield":    {"file": "resources/Predictability/dividend_yield.csv",     "date": "ymd"},
    "loan-fees":         {"file": "resources/Predictability/loan_fees.csv",          "date": "ymd"},
    "portfolios":        {"file": "resources/portfolios/3_portfolios_sorted_by_size.xls", "date": "ymd"},
    "cost-of-equity":    {"file": "resources/cost_of_capital/Consumer.xls",          "date": "myyyy", "col": "Month/Year"},
    # illiquidity-index has no data file; the page carries `no_data: true`.
}


def read_dates(spec: dict) -> tuple[pd.Timestamp, pd.Timestamp]:
    """Return (first, last) observation dates for one dataset."""
    path = STATIC / spec["file"]
    if not path.exists():
        raise FileNotFoundError(path)

    df = pd.read_excel(path) if path.suffix == ".xls" else pd.read_csv(path)

    if spec["date"] == "iso":
        s = pd.to_datetime(df[spec["col"]], errors="coerce")
    elif spec["date"] == "ymd":
        cols = {c.lower(): c for c in df.columns}
        # Portuguese headers appear in some of the older exports.
        y = cols.get("year") or cols["ano"]
        m = cols.get("month") or cols["mes"]
        d = cols.get("day") or cols["dia"]
        s = pd.to_datetime(
            dict(year=df[y].astype(int), month=df[m].astype(int), day=df[d].astype(int)),
            errors="coerce",
        )
    elif spec["date"] == "myyyy":
        s = pd.to_datetime(df[spec["col"]], format="%m/%Y", errors="coerce")
    else:
        raise ValueError(spec["date"])

    s = s.dropna()
    if s.empty:
        raise ValueError(f"no parseable dates in {path}")
    return s.min(), s.max()


def set_field(text: str, key: str, value: str) -> str:
    """Set `key: "value"` in the YAML front matter, inserting it if absent."""
    pattern = re.compile(rf'^{key}:.*$', re.M)
    if pattern.search(text):
        return pattern.sub(f'{key}: "{value}"', text, count=1)
    # insert after the summary block
    m = re.search(r'^summary:.*(?:\n[ \t]+.*)*\n', text, re.M)
    at = m.end() if m else text.index("\n", text.index("---") + 3) + 1
    return text[:at] + f'{key}: "{value}"\n' + text[at:]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="report differences and exit non-zero instead of writing")
    args = ap.parse_args()

    drift = []
    for slug, spec in sorted(SOURCES.items()):
        page = CONTENT / f"{slug}.md"
        if not page.exists():
            print(f"!! {slug}: no content page", file=sys.stderr)
            drift.append(slug)
            continue
        try:
            first, last = read_dates(spec)
        except Exception as exc:                       # noqa: BLE001 — report and continue
            print(f"!! {slug}: {exc}", file=sys.stderr)
            drift.append(slug)
            continue

        text = page.read_text(encoding="utf-8")
        current = re.search(r'^last_observation:\s*"?([\d-]+)', text, re.M)
        current = current.group(1) if current else None
        wanted = last.strftime("%Y-%m-%d")

        if current == wanted:
            print(f"   {slug:18s} {wanted}  ok")
            continue

        drift.append(slug)
        print(f"{'!!' if args.check else '->'} {slug:18s} {current} -> {wanted}")
        if not args.check:
            text = set_field(text, "coverage_start", first.strftime("%Y-%m-%d"))
            text = set_field(text, "last_observation", wanted)
            page.write_text(text, encoding="utf-8")

    if args.check and drift:
        print(f"\n{len(drift)} dataset page(s) disagree with the data files.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
