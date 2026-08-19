#!/usr/bin/env python3
"""Read each filing's DECLARED reporting period from its own cover page.

The filenames under data/raw/ carry a period hint derived from SEC metadata.
For several filers that metadata degenerated to the filing date, so the hint is
off by one to four quarters -- AngloGold's FY2007 20-F sits in a "2008-Q1"
bucket. Any batch extraction that trusts the filename will book annual figures
as quarterly ones.

This module does not trust the filename. It parses the period the document
states about itself, and reports every disagreement.

Two things it deliberately does NOT do:

  * It does not guess. A file whose period cannot be read is reported as
    UNREADABLE, never defaulted to the filename hint -- defaulting would
    reintroduce exactly the error this exists to catch.
  * It does not stop at the first match. "for the year ended December 31, 2002"
    appears in the body of AngloGold's FY2006 20-F as a restatement
    cross-reference; a first-match scan reads it as the report period and is
    wrong by four years. Cover-page patterns are searched in priority order
    within a bounded header window, and body text is never used for annual
    forms.
"""
import html
import pathlib
import re
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data/raw"
HEADER_BYTES = 220_000        # cover page plus a margin for boilerplate
MONTHS = ("january february march april may june july august september "
          "october november december").split()

# Priority order matters: the annual cover phrase must win over any interim
# phrase that also appears in the same document's index or comparatives.
# TR sits second, not last: a transition-report cover is as definitive as an
# annual one, and Gold Fields' Jul-Dec 2010 stub 20-F also contains the phrase
# "six month period ended December 31" in its comparatives. Ordered after H, the
# comparative won and the file was booked to the wrong year.
PATTERNS = [
    ("FY",  r"for\s+the\s+(?:financial|fiscal)\s+year\s+ended[:\s]*([a-z]+\s+\d{1,2},?\s+\d{4})"),
    ("TR",  r"for\s+the\s+transition\s+period\s+from\s+[a-z]+\s+\d{1,2},?\s+\d{4}\s+to\s+([a-z]+\s+\d{1,2},?\s+\d{4})"),
    ("FY",  r"for\s+the\s+year\s+ended[:\s]*([a-z]+\s+\d{1,2},?\s+\d{4})\s*(?:commission|\()"),
    ("Q",   r"for\s+the\s+quarterly\s+period\s+ended[:\s]*([a-z]+\s+\d{1,2},?\s+\d{4})"),
    ("Q",   r"for\s+the\s+(?:quarter|three\s+months)\s+ended[:\s]*([a-z]+\s+\d{1,2},?\s+\d{4})"),
    ("H",   r"for\s+the\s+six\s+months\s+ended[:\s]*([a-z]+\s+\d{1,2},?\s+\d{4})"),
    ("9M",  r"for\s+the\s+nine\s+months\s+ended[:\s]*([a-z]+\s+\d{1,2},?\s+\d{4})"),
]

# Tier 2, for the 92% of files that are EXHIBITS and carry no SEC cover page.
# Heuristic, and labelled as one: take the LATEST period end mentioned anywhere
# in the header window. A results release states its own period alongside the
# prior-year comparative, and its own period is the later of the two. This is
# weaker than a cover read and is never merged with it.
PERIOD_ANY = re.compile(
    r"(three|six|nine)\s+months?\s+(?:period\s+)?ended[:\s]*([a-z]+)\s+(\d{1,2}),?\s+(\d{4})"
    r"|(?:financial\s+|fiscal\s+)?years?\s+ended[:\s]*([a-z]+)\s+(\d{1,2}),?\s+(\d{4})")
SPAN = {"three": "Q", "six": "H", "nine": "9M"}
HINT_RE = re.compile(r"^(\d{4})-Q([1-4])_")


def text_of(path, limit=HEADER_BYTES):
    raw = path.read_text(encoding="utf-8", errors="ignore")[:limit]
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw))).lower()


def declared_period(path):
    """(kind, year, quarter, evidence) or (None, None, None, reason)."""
    if path.suffix.lower() not in (".htm", ".html", ".txt"):
        return None, None, None, "not a text filing"
    try:
        t = text_of(path)
    except Exception as e:                                    # noqa: BLE001
        return None, None, None, f"unreadable: {e}"
    for kind, pat in PATTERNS:
        m = re.search(pat, t)
        if not m:
            continue
        raw_date = m.group(1)
        dm = re.match(r"([a-z]+)\s+(\d{1,2}),?\s+(\d{4})", raw_date)
        if not dm or dm.group(1) not in MONTHS:
            continue
        month, year = MONTHS.index(dm.group(1)) + 1, int(dm.group(3))
        if not (1990 <= year <= 2030):
            continue
        return kind, year, (month - 1) // 3 + 1, raw_date.strip()
    return None, None, None, "no period phrase in header window"


def inferred_period(path):
    """Tier 2. Latest period-end mentioned anywhere in the header window."""
    try:
        t = text_of(path, 300_000)
    except Exception:                                          # noqa: BLE001
        return None, None, None, "unreadable"
    best = None
    for m in PERIOD_ANY.finditer(t):
        span, mon, day, yr = (m.group(1), m.group(2), m.group(3), m.group(4)) \
            if m.group(1) else ("year", m.group(5), m.group(6), m.group(7))
        if mon not in MONTHS:
            continue
        y, mo = int(yr), MONTHS.index(mon) + 1
        if not (1990 <= y <= 2030):
            continue
        key = (y, mo)
        if best is None or key > best[0]:
            best = (key, SPAN.get(span, "FY"), f"{span} months ended {mon} {day}, {yr}")
    if best is None:
        return None, None, None, "no period phrase at all"
    (y, mo), kind, ev = best
    return kind, y, (mo - 1) // 3 + 1, ev


def check(tickers=None, lo=2005, hi=2012):
    rows = []
    for tdir in sorted(RAW.iterdir()):
        if not tdir.is_dir() or (tickers and tdir.name not in tickers):
            continue
        for f in sorted(tdir.iterdir()):
            m = HINT_RE.match(f.name)
            if not m or not (lo <= int(m.group(1)) <= hi):
                continue
            hint_y, hint_q = int(m.group(1)), int(m.group(2))
            kind, year, q, ev = declared_period(f)
            tier = "COVER"
            if kind is None:
                kind, year, q, ev = inferred_period(f)
                tier = "INFERRED" if kind else None
            # An annual form always belongs to Q4 of its own fiscal year.
            want_q = 4 if kind in ("FY", "TR") else q
            agree = (kind is not None) and (year == hint_y) and (want_q == hint_q)
            rows.append({"ticker": tdir.name, "file": f.name, "hint_y": hint_y,
                         "hint_q": hint_q, "tier": tier, "kind": kind, "year": year,
                         "quarter": want_q, "agree": agree, "evidence": ev})
    return rows


def main():
    import pandas as pd
    tickers = sys.argv[1:] or None
    d = pd.DataFrame(check(tickers))
    readable = d[d.kind.notna()]
    cover = d[d.tier == "COVER"]
    bad = readable[~readable.agree]
    print(f"pre-2013 filings scanned: {len(d)}   period recoverable: {len(readable)} "
          f"({len(readable)/max(len(d),1)*100:.0f}%)   of which cover-page: {len(cover)}"
          f"   disagree with filename: {len(bad)}")
    print("\nby ticker (cover = definitive, inferred = heuristic, none = unusable):")
    print(pd.crosstab(d.ticker, d.tier.fillna("none")).to_string())
    print("\ndisagreement rate by tier:")
    print(readable.groupby("tier").agree.agg(
        n="size", agree="sum").assign(
        wrong=lambda x: x.n - x.agree,
        pct=lambda x: (x.wrong / x.n * 100).round(1)).to_string())
    if len(bad):
        print(f"\nfilename period is WRONG for {len(bad)} filings "
              f"(these would be booked to the wrong period):")
        print(bad.groupby(["ticker", "kind"]).size().rename("n").to_string())
        print("\nworst offsets:")
        b = bad.assign(off=(bad.year - bad.hint_y) * 4 + (bad.quarter - bad.hint_q))
        print(b.reindex(b.off.abs().sort_values(ascending=False).index)
               [["ticker", "file", "hint_y", "hint_q", "kind", "year", "quarter", "off"]]
               .head(15).to_string(index=False))
    out = ROOT / "data/final/period_check.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    d.to_csv(out, index=False)
    print(f"\nwrote {out}")
    print("\nUNREADABLE rows are NOT defaulted to the filename hint -- defaulting "
          "would reintroduce the error this check exists to catch.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
