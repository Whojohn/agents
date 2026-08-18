#!/usr/bin/env python3
"""
fetch_gold_price.py
====================

Reproducible downloader for the LBMA gold fix daily price series (1968 ->
present), cached locally so downstream analysis agents never need to hit
prices.lbma.org.uk themselves.

SOURCES (no API key, CORS-open)
--------------------------------
- https://prices.lbma.org.uk/json/gold_pm.json  (PM fix -- primary series)
- https://prices.lbma.org.uk/json/gold_am.json  (AM fix -- backup series,
  used to fill days where the PM fix is missing)

Each record: {"d": "YYYY-MM-DD", "v": [USD, GBP, EUR]}. USD is v[0].

OUTPUTS
-------
- data/raw/lbma_gold_daily.csv
    date, usd_pm, gbp_pm, eur_pm, usd_am, gbp_am, eur_am, usd_resolved,
    resolved_source
  ("usd_resolved" = PM fix when present, else AM fix; "resolved_source"
  records which one was used for that day.)
- data/raw/lbma_gold_quarterly.csv
    quarter, avg_usd, n_days, min_usd, max_usd
  (computed from the PM fix series only, matching how the research team's
  verified checkpoints below were derived.)

VALIDATION
----------
The PM-fix quarterly averages are checked against seven independently
verified checkpoints spanning 2005-2026. Any checkpoint off by more than 1%
FAILS LOUDLY: the script prints a clearly marked FAILURE banner and exits
with a non-zero status. The two known single-day record fixes are also
asserted to appear in the raw PM series.

Idempotent: re-running re-fetches (the LBMA feed is a single always-growing
JSON file, so there is no meaningful "skip" state) but is cheap -- two GETs.
"""

from __future__ import annotations

import csv
import io
import json
import os
import sys
import time
from collections import defaultdict
from datetime import date

import requests

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(REPO_ROOT, "data", "raw")
DAILY_PATH = os.path.join(RAW_DIR, "lbma_gold_daily.csv")
QUARTERLY_PATH = os.path.join(RAW_DIR, "lbma_gold_quarterly.csv")

USER_AGENT = "GoldMarginResearch/1.0 (tdgnhc@gmail.com)"
PM_URL = "https://prices.lbma.org.uk/json/gold_pm.json"
AM_URL = "https://prices.lbma.org.uk/json/gold_am.json"

RETRY_BACKOFFS = [2, 4, 8, 16]

# Research-team-verified checkpoints: PM-fix quarterly average, USD/oz.
CHECKPOINTS = [
    ("2005-Q1", 427.35),
    ("2008-Q3", 871.60),
    ("2011-Q3", 1702.12),
    ("2015-Q4", 1106.45),
    ("2020-Q3", 1908.56),
    ("2024-Q4", 2663.38),
    ("2026-Q2", 4506.29),
]
TOLERANCE_PCT = 1.0  # fail loudly if computed avg differs by more than this

# Known single-day record PM fixes that must appear in the raw series.
RECORD_FIXES = [
    ("2011-09-05", 1895.00),
    ("2020-08-06", 2067.15),
]
RECORD_FIX_TOLERANCE_PCT = 0.5


def http_get_json(url: str) -> list:
    last_exc = None
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    for attempt in range(len(RETRY_BACKOFFS) + 1):
        try:
            resp = session.get(url, timeout=60)
            resp.raise_for_status()
            return resp.json()
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            last_exc = e
            if attempt < len(RETRY_BACKOFFS):
                backoff = RETRY_BACKOFFS[attempt]
                print(f"  retry {attempt + 1}/{len(RETRY_BACKOFFS)} in {backoff}s for {url} ({e})")
                time.sleep(backoff)
    raise RuntimeError(f"Failed to fetch {url} after retries: {last_exc}")


def quarter_of(d: date) -> str:
    q = (d.month - 1) // 3 + 1
    return f"{d.year}-Q{q}"


def main() -> int:
    os.makedirs(RAW_DIR, exist_ok=True)

    print(f"Fetching PM fix series: {PM_URL}")
    pm_records = http_get_json(PM_URL)
    print(f"  {len(pm_records)} daily records")

    print(f"Fetching AM fix series (backup): {AM_URL}")
    am_records = http_get_json(AM_URL)
    print(f"  {len(am_records)} daily records")

    pm_by_date: dict[str, list] = {r["d"]: r["v"] for r in pm_records}
    am_by_date: dict[str, list] = {r["d"]: r["v"] for r in am_records}

    all_dates = sorted(set(pm_by_date) | set(am_by_date))

    # --- Build & write the daily series -------------------------------
    daily_rows = []
    for d in all_dates:
        pm_v = pm_by_date.get(d)
        am_v = am_by_date.get(d)
        usd_pm = pm_v[0] if pm_v else None
        gbp_pm = pm_v[1] if pm_v else None
        eur_pm = pm_v[2] if pm_v else None
        usd_am = am_v[0] if am_v else None
        gbp_am = am_v[1] if am_v else None
        eur_am = am_v[2] if am_v else None

        if usd_pm is not None:
            usd_resolved, source = usd_pm, "pm"
        elif usd_am is not None:
            usd_resolved, source = usd_am, "am"
        else:
            usd_resolved, source = None, "none"

        daily_rows.append(
            {
                "date": d,
                "usd_pm": usd_pm,
                "gbp_pm": gbp_pm,
                "eur_pm": eur_pm,
                "usd_am": usd_am,
                "gbp_am": gbp_am,
                "eur_am": eur_am,
                "usd_resolved": usd_resolved,
                "resolved_source": source,
            }
        )

    with open(DAILY_PATH, "w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "date", "usd_pm", "gbp_pm", "eur_pm", "usd_am", "gbp_am",
                "eur_am", "usd_resolved", "resolved_source",
            ],
        )
        w.writeheader()
        for r in daily_rows:
            w.writerow(r)
    print(f"Wrote daily series: {DAILY_PATH} ({len(daily_rows)} rows, "
          f"{all_dates[0]}..{all_dates[-1]})")

    # --- Resample to quarterly means (PM fix only, matching checkpoints) --
    quarterly_pm: dict[str, list] = defaultdict(list)
    for d, v in pm_by_date.items():
        if v and v[0] is not None:
            y, m, day = (int(x) for x in d.split("-"))
            quarterly_pm[quarter_of(date(y, m, day))].append(v[0])

    quarterly_rows = []
    for q in sorted(quarterly_pm.keys()):
        vals = quarterly_pm[q]
        quarterly_rows.append(
            {
                "quarter": q,
                "avg_usd": round(sum(vals) / len(vals), 4),
                "n_days": len(vals),
                "min_usd": min(vals),
                "max_usd": max(vals),
            }
        )

    with open(QUARTERLY_PATH, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["quarter", "avg_usd", "n_days", "min_usd", "max_usd"])
        w.writeheader()
        for r in quarterly_rows:
            w.writerow(r)
    print(f"Wrote quarterly series: {QUARTERLY_PATH} ({len(quarterly_rows)} quarters)")

    # --- Validation ------------------------------------------------------
    quarterly_by_label = {r["quarter"]: r for r in quarterly_rows}
    failures = []
    checkpoint_results = []
    for q, expected in CHECKPOINTS:
        row = quarterly_by_label.get(q)
        if row is None:
            failures.append(f"{q}: NO DATA COMPUTED (expected PM avg ~{expected})")
            checkpoint_results.append((q, expected, None, None, False))
            continue
        computed = row["avg_usd"]
        diff_pct = 100.0 * (computed - expected) / expected
        ok = abs(diff_pct) <= TOLERANCE_PCT
        checkpoint_results.append((q, expected, computed, diff_pct, ok))
        if not ok:
            failures.append(
                f"{q}: computed PM avg ${computed:.2f} vs expected ${expected:.2f} "
                f"({diff_pct:+.3f}%) -- EXCEEDS {TOLERANCE_PCT}% tolerance"
            )

    record_fix_results = []
    for d, expected in RECORD_FIXES:
        v = pm_by_date.get(d)
        actual = v[0] if v else None
        if actual is None:
            failures.append(f"record fix {d}: NO PM RECORD FOUND (expected ~{expected})")
            record_fix_results.append((d, expected, None, False))
            continue
        diff_pct = 100.0 * (actual - expected) / expected
        ok = abs(diff_pct) <= RECORD_FIX_TOLERANCE_PCT
        record_fix_results.append((d, expected, actual, ok))
        if not ok:
            failures.append(
                f"record fix {d}: PM fix ${actual:.2f} vs expected ${expected:.2f} "
                f"({diff_pct:+.3f}%) -- EXCEEDS {RECORD_FIX_TOLERANCE_PCT}% tolerance"
            )

    print("\n=== QUARTERLY CHECKPOINT VALIDATION (PM fix, tolerance "
          f"{TOLERANCE_PCT}%) ===")
    for q, expected, computed, diff_pct, ok in checkpoint_results:
        status = "PASS" if ok else "FAIL"
        computed_s = f"${computed:.2f}" if computed is not None else "N/A"
        diff_s = f"{diff_pct:+.3f}%" if diff_pct is not None else "N/A"
        print(f"  [{status}] {q}: expected ${expected:.2f}  computed {computed_s}  diff {diff_s}")

    print("\n=== RECORD-FIX ASSERTIONS ===")
    for d, expected, actual, ok in record_fix_results:
        status = "PASS" if ok else "FAIL"
        actual_s = f"${actual:.2f}" if actual is not None else "N/A"
        print(f"  [{status}] {d}: expected ${expected:.2f}  actual {actual_s}")

    if failures:
        print("\n" + "!" * 78)
        print("!!! GOLD PRICE VALIDATION FAILED -- DO NOT TRUST DOWNSTREAM RESULTS !!!")
        print("!" * 78)
        for f in failures:
            print(f"  - {f}")
        print("!" * 78)
        return 1

    print("\nAll checkpoints and record fixes PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
