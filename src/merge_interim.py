#!/usr/bin/env python3
"""
merge_interim.py
================

Fold a per-era extraction CSV (``<T>_2017_2020.csv``) into the canonical
per-company file that ``build_series.py`` actually reads
(``<T>_quarterly.csv`` / ``<T>_halfyearly.csv`` / ``<T>_mixed.csv``).

WHY THIS EXISTS
---------------
The 2013-2016 era was folded in by hand. That worked for four files. Six
land at once now, and a hand merge has three silent failure modes:

1. **Silent overwrite.** An era file that repeats a period the canonical
   file already holds will, under any naive concatenate-and-dedupe, quietly
   replace a verified row with an unverified one. Here a repeated period is
   compared field by field and, if the values disagree, the merge STOPS and
   prints the disagreement. Two extractions of the same quarter that differ
   is news, not a merge conflict to resolve by fiat.

2. **Column-set drift.** The six canonical files do NOT share a header: 30
   columns are common, 38 appear across the union, and each company carries
   its own extras (Barrick's ``segment_revenue_gold_consolidated`` is what
   ``REVENUE_BASIS`` reads for it; Agnico's ``aisc_denominator_oz`` is what
   restates its per-ounce-produced AISC). So header equality is the WRONG
   test -- it would reject a perfectly good era file for lacking a column its
   company never uses. The merge takes the union, fills the absent side with
   empty, and PRINTS which columns each side lacked. Empty is the honest
   value there, and the fidelity grading reads it as the gap it is; what
   would be dishonest is doing it silently.

3. **Frequency drift in the filename.** The canonical filename encodes the
   frequency, and ``build_series.py`` globs on it. If an era file brings a
   half-year row into a file named ``_quarterly.csv``, the row is loaded but
   the NAME now lies. Worse, if it brings a quarterly row into
   ``_halfyearly.csv``, the same. This script renames the canonical file to
   ``_mixed.csv`` when the merged set actually contains both, so the glob
   and the contents stay in agreement.

4. **Collation.** ``'H'(72) < 'Q'(81)`` in ASCII, so a plain string sort puts
   ``2021H2`` BEFORE ``2021Q1`` and silently reverses a company's own history
   for every downstream window function. Rows are ordered on a real
   chronological key, never on the period string.

USAGE
-----
    python3 src/merge_interim.py --dry-run          # show what would change
    python3 src/merge_interim.py                    # merge every era file
    python3 src/merge_interim.py --ticker GFI       # one company
    python3 src/merge_interim.py --prefer era       # on conflict, era wins
    python3 src/merge_interim.py --prefer canonical # on conflict, keep old

Without ``--prefer``, a value conflict is a hard stop. That is the point.
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import sys
from pathlib import Path

INTERIM = Path(__file__).resolve().parent.parent / "data" / "interim"

ERA_RE = re.compile(r"^([A-Z]+)_(\d{4})_(\d{4})\.csv$")
CANON_SUFFIXES = ("_quarterly.csv", "_halfyearly.csv", "_mixed.csv")

# Fields excluded from the conflict test: they are provenance and bookkeeping,
# not claims about the world. Two agents citing different (both valid) source
# files for the same figure is not a disagreement about the figure.
PROVENANCE_FIELDS = {"source_file"}


def period_freq(period: str) -> str:
    """'2021Q3' -> 'Q'; '2021H1' -> 'H'."""
    return "H" if "H" in str(period)[4:] else "Q"


def period_start_month(period: str) -> int:
    """First month of the period, 1-12. Q3 -> 7; H2 -> 7."""
    p = str(period)
    n = int(p[5])
    return (n - 1) * 6 + 1 if period_freq(p) == "H" else (n - 1) * 3 + 1


def period_order(period: str) -> int:
    """Chronological sort key. See failure mode 4 in the module docstring."""
    return int(str(period)[:4]) * 100 + period_start_month(period)


def read_csv(path: Path) -> tuple[list[str], list[dict]]:
    with path.open(newline="") as fh:
        r = csv.DictReader(fh)
        return list(r.fieldnames or []), list(r)


def canonical_path(ticker: str) -> Path | None:
    for suf in CANON_SUFFIXES:
        p = INTERIM / f"{ticker}{suf}"
        if p.exists():
            return p
    return None


def describe_conflict(period: str, a: dict, b: dict) -> list[str]:
    """Every field where two rows for the same period actually disagree."""
    out = []
    for k in a:
        if k in PROVENANCE_FIELDS:
            continue
        va, vb = (a.get(k) or "").strip(), (b.get(k) or "").strip()
        if va == vb:
            continue
        # Numerically equal but differently formatted is not a conflict.
        try:
            if float(va) == float(vb):
                continue
        except ValueError:
            pass
        out.append(f"      {k:26} canonical={va!r:>18}   era={vb!r}")
    return out


def merge_ticker(ticker: str, era_files: list[Path], prefer: str | None,
                 dry_run: bool) -> bool:
    canon = canonical_path(ticker)
    if canon is None:
        print(f"[{ticker}] no canonical file yet -- will create from era files")
        header, rows = [], []
    else:
        header, rows = read_csv(canon)

    by_period = {r["quarter"]: r for r in rows}
    n_before = len(by_period)
    added = updated = identical = 0
    conflicts: list[str] = []

    for ef in era_files:
        eh, erows = read_csv(ef)
        only_era = [c for c in eh if c not in header]
        only_can = [c for c in header if c not in eh]
        if only_can:
            print(f"[{ticker}] {ef.name} has no column for: {only_can}")
            print(f"         -> empty on its {len(erows)} rows; the fidelity "
                  f"grading will read that as the gap it is")
        if only_era:
            print(f"[{ticker}] {ef.name} brings new columns: {only_era}")
            print(f"         -> empty on the {len(rows)} rows already held")
        header = header + only_era

        for row in erows:
            per = row["quarter"]
            if per not in by_period:
                by_period[per] = row
                added += 1
                continue
            diff = describe_conflict(per, by_period[per], row)
            if not diff:
                identical += 1
                continue
            if prefer is None:
                conflicts.append(f"  {ticker} {per}  ({ef.name})")
                conflicts.extend(diff)
            elif prefer == "era":
                by_period[per] = row
                updated += 1
            else:
                updated += 0  # canonical kept

    if conflicts:
        print(f"\n[{ticker}] STOPPING -- {len(era_files)} era file(s) restate "
              f"periods the canonical file already holds, with different values:",
              file=sys.stderr)
        for line in conflicts:
            print(line, file=sys.stderr)
        print("\n  Two independent extractions of the same period disagreeing is a\n"
              "  finding, not a merge nuisance. Read both before choosing.\n"
              "  Re-run with --prefer era or --prefer canonical once you have.",
              file=sys.stderr)
        return False

    merged = sorted(by_period.values(), key=lambda r: period_order(r["quarter"]))
    for r in merged:                       # square every row to the union
        for c in header:
            r.setdefault(c, "")
    freqs = {period_freq(r["quarter"]) for r in merged}
    suffix = ("_mixed.csv" if len(freqs) > 1
              else "_quarterly.csv" if freqs == {"Q"} else "_halfyearly.csv")
    target = INTERIM / f"{ticker}{suffix}"

    span = f"{merged[0]['quarter']}..{merged[-1]['quarter']}" if merged else "-"
    rename = canon is not None and canon != target
    print(f"[{ticker}] {n_before} -> {len(merged)} rows  (+{added} new, "
          f"{identical} identical, {updated} replaced)  {span}  freq={''.join(sorted(freqs))}")
    if rename:
        print(f"[{ticker}] RENAME {canon.name} -> {target.name}  "
              f"(merged set now holds {'/'.join(sorted(freqs))} rows)")

    if dry_run:
        return True

    with target.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=header)
        w.writeheader()
        w.writerows(merged)
    if rename and canon.exists():
        canon.unlink()
    for ef in era_files:
        shutil.move(str(ef), str(INTERIM / "merged" / ef.name))
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", default=None, help="only this company")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--prefer", choices=("era", "canonical"), default=None,
                    help="resolve value conflicts instead of stopping")
    args = ap.parse_args()

    era: dict[str, list[Path]] = {}
    for p in sorted(INTERIM.glob("*.csv")):
        m = ERA_RE.match(p.name)
        if not m:
            continue
        t = m.group(1)
        if args.ticker and t != args.ticker.upper():
            continue
        era.setdefault(t, []).append(p)

    if not era:
        print("no era files to merge")
        return 0

    if not args.dry_run:
        (INTERIM / "merged").mkdir(exist_ok=True)

    ok = True
    for t in sorted(era):
        if not merge_ticker(t, era[t], args.prefer, args.dry_run):
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
