#!/usr/bin/env python3
"""
build_sources.py
================

Turn every ``source_file`` string in ``data/interim/`` into a citation a reader
can act on: form type, filing date, accession number, a direct SEC EDGAR URL,
and the SHA-256 of the exact bytes this project read.

WHY THIS EXISTS
---------------
The page told the reader WHICH STATEMENT each figure came from ("Costs
applicable to sales", "Revenues - as adjusted") and never once told them WHICH
FILING. That is a citation without a reference: it cannot be checked without
first guessing which of a company's ~120 filings was meant. Section B of the
extraction contract has demanded ``src_file`` on every number from the start,
and the extractions supplied it -- 760 references across 478 observations, not
one missing. Nothing downstream had ever read the column.

WHAT MAKES THE URL TRUSTWORTHY
------------------------------
It is not constructed from a guessed pattern. ``data/raw/manifest.csv`` is the
fetcher's own record of what it downloaded, and it carries the CIK, accession,
exhibit filename, byte count and SHA-256 for all 6,880 documents. Every one of
the 760 references joins to it. The URL is then assembled from the manifest's
own cik + accession + exhibit_filename, and a sample of twelve was checked
against live EDGAR: all returned 200 and every Content-Length matched the
manifest byte count exactly. So a reader who downloads the file and hashes it
gets the same digest printed here, or the file is not the one this project read.

TWO OUTPUTS, BECAUSE THERE ARE TWO QUESTIONS
--------------------------------------------
- ``来源清单_文件.csv`` -- one row per document. "Give me everything you read."
- ``来源清单_观测.csv`` -- one row per observation-document pair. "Where did
  THIS quarter's number come from?"

AngloGold appears under two CIKs (1067428 before the 2023 UK redomicile,
1973832 after). That is not an error to normalise away -- the pre-2023 filings
genuinely live under the old CIK and the URL has to use it.
"""

from __future__ import annotations

import glob
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INTERIM, FINAL, RAW = ROOT / "data/interim", ROOT / "data/final", ROOT / "data/raw"

# A source_file cell is not always a bare path. 86 of them wrap the path in
# prose ("gold rev (FY anchor): data/raw/AEM/... (2016 filing's 3-yr table)"),
# and some carry two or three paths in one cell. Splitting on a delimiter loses
# those; finding every path-shaped substring does not.
PATH_RE = re.compile(
    r"data/raw/([A-Z]+)/([0-9]{4}-(?:Q[1-4]|H[12]|FY))_(\d{10}-\d{2}-\d{6})"
    r"_([A-Za-z0-9._\-]+?\.(?:htm|html|txt|pdf))")

EDGAR = "https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/{doc}"
EDGAR_INDEX = "https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/{dashed}-index.htm"


def collect_references() -> pd.DataFrame:
    rows = []
    for f in sorted(glob.glob(str(INTERIM / "*_*.csv"))):
        if "prelim" in f:
            continue
        d = pd.read_csv(f)
        if "source_file" not in d.columns:
            continue
        for _, r in d.iterrows():
            found = PATH_RE.findall(str(r.source_file))
            if not found:
                rows.append({"ticker": str(r.ticker).split("/")[0], "quarter": r.quarter,
                             "local_path": None, "raw": str(r.source_file)[:200]})
                continue
            for t, per, acc, doc in found:
                rows.append({"ticker": str(r.ticker).split("/")[0], "quarter": r.quarter,
                             "local_path": f"data/raw/{t}/{per}_{acc}_{doc}", "raw": None})
    return pd.DataFrame(rows).drop_duplicates(["ticker", "quarter", "local_path"])


def main() -> int:
    refs = collect_references()
    unparsed = refs[refs.local_path.isna()]
    refs = refs[refs.local_path.notna()].drop(columns="raw")

    man = pd.read_csv(RAW / "manifest.csv")
    j = refs.merge(man[["local_path", "cik", "form", "filing_date", "report_date",
                        "accession", "exhibit_filename", "bytes", "sha256"]],
                   on="local_path", how="left")

    missing = j[j.cik.isna()]
    if len(missing):
        # Loud, not silent: a reference the fetcher has no record of cannot be
        # given a URL, and publishing it without one would look like a citation.
        print(f"WARNING: {len(missing)} reference(s) not in the fetch manifest -- "
              f"no URL can be built for these:", file=sys.stderr)
        print(missing[["ticker", "quarter", "local_path"]].to_string(index=False),
              file=sys.stderr)
    j = j[j.cik.notna()].copy()
    j["cik"] = j.cik.astype(int)
    j["acc_nodash"] = j.accession.str.replace("-", "", regex=False)
    j["url"] = [EDGAR.format(cik=c, acc=a, doc=d)
                for c, a, d in zip(j.cik, j.acc_nodash, j.exhibit_filename)]
    j["url_index"] = [EDGAR_INDEX.format(cik=c, acc=a, dashed=n)
                      for c, a, n in zip(j.cik, j.acc_nodash, j.accession)]

    obs_cols = ["ticker", "quarter", "form", "filing_date", "report_date", "cik",
                "accession", "exhibit_filename", "bytes", "sha256", "url",
                "url_index", "local_path"]
    obs = j[obs_cols].sort_values(["ticker", "quarter", "filing_date"])
    obs.to_csv(FINAL / "来源清单_观测.csv", index=False)

    files = (j.drop_duplicates("local_path")
              [["ticker", "form", "filing_date", "report_date", "cik", "accession",
                "exhibit_filename", "bytes", "sha256", "url", "url_index", "local_path"]]
              .sort_values(["ticker", "filing_date", "exhibit_filename"]))
    # Which observations each document supports -- the reverse lookup, so a
    # reader holding one filing can see everything it was used for.
    used = (j.groupby("local_path")
             .apply(lambda g: ";".join(sorted(set(g.ticker + " " + g.quarter))),
                    include_groups=False)
             .rename("used_for"))
    files = files.join(used, on="local_path")
    files.to_csv(FINAL / "来源清单_文件.csv", index=False)

    print(f"来源清单: {len(obs)} 条观测-文档引用, {len(files)} 份唯一文档, "
          f"{j.accession.nunique()} 份唯一申报, {len(unparsed)} 条无法解析")
    print(files.form.value_counts().rename("按表格类型").to_string())
    cov = (obs.groupby("ticker")
              .agg(引用=("local_path", "size"), 唯一文档=("local_path", "nunique"),
                   覆盖期数=("quarter", "nunique")))
    print(cov.to_string())

    panel = pd.read_csv(FINAL / "margins.csv")
    have = set(zip(obs.ticker, obs.quarter))
    gaps = [(t, q) for t, q in zip(panel.ticker, panel.quarter) if (t, q) not in have]
    if gaps:
        print(f"\n{len(gaps)} 个已发布观测没有任何可解析的来源引用:")
        for t, q in gaps[:20]:
            print(f"   {t} {q}")
    else:
        print(f"\n面板 {len(panel)} 个观测全部有可解析、可下载的来源引用。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
