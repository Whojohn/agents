#!/usr/bin/env python3
"""
fetch_filings.py
=================

Reproducible downloader for quarterly / annual earnings-release exhibits and
interim & annual financial-statement filings for six gold miners, 2021Q1-2026Q2,
from SEC EDGAR.

WHY THIS EXISTS
---------------
Downstream analysis agents must parse LOCAL files, never hit the network.
This script is the single source of truth for what gets cached under
data/raw/<TICKER>/ and data/raw/manifest.csv.

WHAT IT PULLS PER COMPANY
--------------------------
- Newmont (NEM, CIK 1164727):
    * 8-K (Item 2.02 only) + EX-99.x  -> quarterly press release / operating
      stats (the AISC/production "checksum" source).
    * 10-Q, 10-K                      -> the ACTUAL financial statements
      (segment revenue/cost note, revenue disaggregation, cash flow
      statement). Newmont is a US domestic filer, so these never appear as
      8-K exhibits.
- Barrick (GOLD, CIK 756894), Agnico Eagle (AEM, CIK 2809),
  Kinross (KGC, CIK 701818): 6-K (all exhibits incl. MD&A + interim
  financial statements) + 40-F (annual, audited segment note anchor).
- AngloGold Ashanti (AU): STITCHED across two CIKs because the company
  redomiciled to the UK in Sept 2023 and got a new CIK.
    * OLD entity CIK 0001067428 (pre-redomiciliation, files run through
      ~2023-10-05)
    * NEW entity CIK 0001973832 (plc, files start ~2023-04-21 -- there is a
      several-month overlap while both entities filed)
  Both CIKs' 6-K + 20-F filings land in the same data/raw/AU/ folder.
- Gold Fields (GFI, CIK 1172724): 6-K + 20-F. Full cost/capex detail is only
  in H1 and FY releases per research-team note; we fetch every quarter's 6-K
  regardless since AngloGold/Gold Fields still publish per-quarter operating
  stats + condensed financials even when the "full" cost breakdown doesn't
  appear every quarter.

CLASSIFICATION (metadata only -- no figures are parsed)
---------------------------------------------------------
Every downloaded exhibit is scanned for two independent keyword families and
tagged with booleans:
  - has_operating_stats:      AISC / total cash cost / ounces produced / ...
  - has_financial_statements: condensed consolidated statements / segment
                               information / disaggregation of revenue / ...
This is a *cataloguing* aid (which local file has what) -- it never extracts
or computes a financial figure. That is a downstream agent's job.

USAGE
-----
    python3 src/fetch_filings.py [--limit N] [--tickers NEM,GOLD,...]

Idempotent: re-running skips any exhibit already on disk (verified by
recomputing its local sha256) and only fetches what's missing.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import hashlib
import io
import json
import logging
import os
import re
import sys
import threading
import time
from dataclasses import dataclass, field

import requests
from datetime import date
from typing import Optional

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------

USER_AGENT = "GoldMarginResearch/1.0 (tdgnhc@gmail.com)"
HEADERS = {"User-Agent": USER_AGENT}
_SESSION = requests.Session()
_SESSION.headers.update(HEADERS)

START_DATE = date(2021, 1, 1)
END_DATE = date(2026, 8, 18)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(REPO_ROOT, "data", "raw")
MANIFEST_PATH = os.path.join(RAW_DIR, "manifest.csv")
COVERAGE_PATH = os.path.join(RAW_DIR, "coverage_matrix.csv")
LOG_PATH = os.path.join(RAW_DIR, "fetch_filings.log")

MIN_EXHIBIT_BYTES = 8_000   # "~20KB" threshold from the brief, lowered after
                             # verification: a real Gold Fields H1-2026
                             # trading-statement/operating-update exhibit
                             # (containing genuine AISC/production/EPS
                             # figures) was found at 12,065 bytes -- i.e.
                             # below the naive ~15-20KB cutoff. The generic
                             # 6-K "cover" boilerplate docs that the size
                             # filter is meant to exclude were empirically
                             # observed clustering at exactly ~15.0-15.5KB,
                             # so 8KB still screens those out while no
                             # longer dropping short-but-substantive
                             # exhibits like trading statements.
KEEP_EXTENSIONS = {".htm", ".html", ".pdf"}

RATE_LIMIT_PER_SEC = 5.0
MAX_WORKERS = 8
RETRY_BACKOFFS = [2, 4, 8, 16]  # seconds

# ---- company / CIK registry -----------------------------------------------

@dataclass
class Company:
    ticker: str
    name: str
    ciks: list[str]
    quarterly_forms: list[str]      # e.g. ["8-K"] or ["6-K"]
    annual_forms: list[str]         # e.g. ["10-K"], ["40-F"], ["20-F"]
    extra_forms: list[str] = field(default_factory=list)  # e.g. Newmont 10-Q


COMPANIES: list[Company] = [
    Company(
        ticker="NEM",
        name="Newmont Corporation",
        ciks=["0001164727"],
        quarterly_forms=["8-K"],
        annual_forms=["10-K"],
        extra_forms=["10-Q"],
    ),
    Company(
        ticker="GOLD",
        name="Barrick Mining Corp",
        ciks=["0000756894"],
        quarterly_forms=["6-K"],
        annual_forms=["40-F"],
    ),
    Company(
        ticker="AEM",
        name="Agnico Eagle Mines Ltd",
        ciks=["0000002809"],
        quarterly_forms=["6-K"],
        annual_forms=["40-F"],
    ),
    Company(
        ticker="AU",
        name="AngloGold Ashanti (stitched: old CIK 1067428 + new CIK 1973832)",
        ciks=["0001973832", "0001067428"],  # new entity first, old entity second
        quarterly_forms=["6-K"],
        annual_forms=["20-F"],
    ),
    Company(
        ticker="KGC",
        name="Kinross Gold Corp",
        ciks=["0000701818"],
        quarterly_forms=["6-K"],
        annual_forms=["40-F"],
    ),
    Company(
        ticker="GFI",
        name="Gold Fields Ltd",
        ciks=["0001172724"],
        quarterly_forms=["6-K"],
        annual_forms=["20-F"],
    ),
]

# ---- content classification keyword banks ----------------------------------

FIN_STMT_KEYWORDS = [
    "condensed consolidated statements",
    "condensed consolidated income",
    "condensed consolidated balance sheet",
    "consolidated statements of income",
    "consolidated statements of operations",
    "consolidated income statement",
    "consolidated balance sheet",
    "statement of financial position",
    "statements of financial position",
    "consolidated statements of cash flow",
    "statements of cash flows",
    "cash flow statement",
    "segment information",
    "segment note",
    "notes to the condensed",
    "notes to the consolidated",
    "notes to financial statements",
    "notes to the financial statements",
    "disaggregation of revenue",
    "revenue by segment",
    "management's discussion and analysis",
    "results of consolidated operations",
]

OPS_STATS_KEYWORDS = [
    "all-in sustaining cost",
    "all-in sustaining costs",
    "total cash cost",
    "total cash costs",
    "cash cost per ounce",
    "ounces produced",
    "gold produced",
    "production statistics",
    "operating statistics",
    "tonnes milled",
    "ore mined",
    "realized price",
    "realised price",
    "cost applicable to sales",
]

MIN_KEYWORD_HITS = 2  # distinct phrases, not raw occurrences


# --------------------------------------------------------------------------
# Logging
# --------------------------------------------------------------------------

os.makedirs(RAW_DIR, exist_ok=True)
logger = logging.getLogger("fetch_filings")
logger.setLevel(logging.INFO)
_fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S")
_sh = logging.StreamHandler(sys.stdout)
_sh.setFormatter(_fmt)
logger.addHandler(_sh)
_fh = logging.FileHandler(LOG_PATH, mode="w")
_fh.setFormatter(_fmt)
logger.addHandler(_fh)


# --------------------------------------------------------------------------
# Rate limiter + HTTP helpers
# --------------------------------------------------------------------------

class RateLimiter:
    """Global token gate: no more than RATE_LIMIT_PER_SEC requests/sec across
    all threads, regardless of how many workers are in flight."""

    def __init__(self, per_sec: float):
        self.min_interval = 1.0 / per_sec
        self._lock = threading.Lock()
        self._next_ok = 0.0

    def wait(self):
        with self._lock:
            now = time.monotonic()
            start = max(now, self._next_ok)
            self._next_ok = start + self.min_interval
            sleep_for = start - now
        if sleep_for > 0:
            time.sleep(sleep_for)


_limiter = RateLimiter(RATE_LIMIT_PER_SEC)


class FetchError(RuntimeError):
    pass


def _request(url: str, timeout: float = 60.0) -> bytes:
    resp = _SESSION.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.content


def http_get(url: str, retries: int = len(RETRY_BACKOFFS) + 1) -> bytes:
    """GET with self-throttling + exponential-backoff retry."""
    last_exc: Optional[Exception] = None
    for attempt in range(retries):
        _limiter.wait()
        try:
            return _request(url)
        except requests.exceptions.HTTPError as e:
            last_exc = e
            code = e.response.status_code if e.response is not None else None
            if code in (403, 404) and attempt == 0:
                # log once immediately, still retry (SEC occasionally 403s
                # transiently even with a correct UA under load)
                logger.warning(f"HTTP {code} on {url}")
            if code == 404:
                # Not found is not going to fix itself with a retry.
                raise FetchError(f"404 Not Found: {url}") from e
        except (requests.exceptions.RequestException, TimeoutError, ConnectionError, OSError) as e:
            last_exc = e
        if attempt < len(RETRY_BACKOFFS):
            backoff = RETRY_BACKOFFS[attempt]
            logger.warning(
                f"retry {attempt + 1}/{len(RETRY_BACKOFFS)} in {backoff}s "
                f"for {url} ({last_exc})"
            )
            time.sleep(backoff)
    raise FetchError(f"Failed after {retries} attempts: {url} ({last_exc})")


def http_get_json(url: str) -> dict:
    return json.loads(http_get(url).decode("utf-8"))


# --------------------------------------------------------------------------
# EDGAR submissions listing
# --------------------------------------------------------------------------

def fetch_all_filings_for_cik(cik: str) -> list[dict]:
    """Return every filing entry (dict with accessionNumber/form/filingDate/
    reportDate/primaryDocument/size) for this CIK whose filingDate could
    plausibly fall in [START_DATE, END_DATE]. Follows filings.files[] when
    the inline 'recent' block doesn't reach back far enough -- reproducible
    even years from now when 'recent' windows have rolled forward."""
    cik10 = cik.zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{cik10}.json"
    data = http_get_json(url)
    filings_block = data["filings"]
    recent = filings_block["recent"]
    all_rows = _rows_from_block(recent, cik)

    earliest_recent = min((r["filingDate"] for r in all_rows), default=None)
    if earliest_recent is None or earliest_recent > START_DATE.isoformat():
        for extra in filings_block.get("files", []):
            # each entry: {"name":..., "filingFrom":..., "filingTo":...}
            if extra.get("filingTo", "9999-99-99") < START_DATE.isoformat():
                continue
            extra_url = f"https://data.sec.gov/submissions/{extra['name']}"
            try:
                extra_data = http_get_json(extra_url)
            except FetchError as e:
                logger.error(f"could not fetch older submissions file: {e}")
                continue
            # older-file JSONs are themselves flat arrays under the same keys
            all_rows.extend(_rows_from_block(extra_data, cik))
            logger.info(f"  CIK {cik}: pulled additional history from {extra['name']}")

    return all_rows


def _rows_from_block(block: dict, cik: str) -> list[dict]:
    n = len(block["form"])
    rows = []
    for i in range(n):
        fdate = block["filingDate"][i]
        rows.append(
            {
                "cik": cik,
                "accessionNumber": block["accessionNumber"][i],
                "filingDate": fdate,
                "reportDate": block["reportDate"][i] if block.get("reportDate") else "",
                "form": block["form"][i],
                "items": (block.get("items") or [""] * n)[i],
                "primaryDocument": block["primaryDocument"][i],
                "primaryDocDescription": (block.get("primaryDocDescription") or [""] * n)[i],
                "size": block["size"][i] if block.get("size") else 0,
            }
        )
    return rows


# --------------------------------------------------------------------------
# Filing index page parsing
# --------------------------------------------------------------------------

_TABLE_RE = re.compile(
    r'<table class="tableFile" summary="Document Format Files">(.*?)</table>', re.S
)
_ROW_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
_CELL_RE = re.compile(r"<td[^>]*>(.*?)</td>", re.S)
_TAG_RE = re.compile(r"<[^>]+>")
_HREF_RE = re.compile(r'href="([^"]+)"')


def list_index_documents(cik: str, accession: str) -> list[dict]:
    """Parse the EDGAR filing index page and return each document row:
    {seq, description, filename, href, doc_type, size}."""
    cik_int = str(int(cik))
    acc_nodash = accession.replace("-", "")
    idx_url = (
        f"https://www.sec.gov/Archives/edgar/data/{cik_int}/{acc_nodash}/"
        f"{accession}-index.htm"
    )
    html = http_get(idx_url).decode("utf-8", errors="ignore")
    m = _TABLE_RE.search(html)
    if not m:
        return []
    docs = []
    for row_html in _ROW_RE.findall(m.group(1)):
        cells = _CELL_RE.findall(row_html)
        if not cells or len(cells) < 5:
            continue
        href_match = _HREF_RE.search(cells[2])
        text_cells = [re.sub(r"&nbsp;|&#160;", " ", _TAG_RE.sub(" ", c)).strip() for c in cells]
        seq, desc, doc_cell, doc_type, size_s = text_cells[:5]
        if not href_match:
            continue
        href = href_match.group(1)
        filename = href.rsplit("/", 1)[-1]
        try:
            size = int(size_s.strip())
        except ValueError:
            size = 0
        # /ix?doc=/Archives/... -> strip the inline-XBRL viewer wrapper
        if href.startswith("/ix?doc="):
            href = href.split("/ix?doc=", 1)[1]
        if href.startswith("/"):
            href = f"https://www.sec.gov{href}"
        docs.append(
            {
                "seq": seq,
                "description": desc,
                "filename": filename,
                "url": href,
                "doc_type": doc_type,
                "size": size,
            }
        )
    return docs


# --------------------------------------------------------------------------
# Content classification
# --------------------------------------------------------------------------

def _extract_text_htm(raw: bytes) -> str:
    html = raw.decode("utf-8", errors="ignore")
    text = _TAG_RE.sub(" ", html)
    text = re.sub(r"&nbsp;|&#160;", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower()


def _extract_text_pdf(raw: bytes, max_pages: int = 10) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        return ""
    try:
        reader = PdfReader(io.BytesIO(raw))
        chunks = []
        for page in reader.pages[:max_pages]:
            chunks.append(page.extract_text() or "")
        return " ".join(chunks).lower()
    except Exception:
        return ""


def classify_content(raw: bytes, filename: str) -> tuple[bool, bool]:
    """Metadata-only cataloguing: does this document LOOK LIKE it contains
    operating statistics and/or financial statements? Pure keyword presence
    -- no figures are read, computed, or stored."""
    ext = os.path.splitext(filename)[1].lower()
    if ext in (".htm", ".html"):
        text = _extract_text_htm(raw)
    elif ext == ".pdf":
        text = _extract_text_pdf(raw)
    else:
        text = ""
    fin_hits = sum(1 for kw in FIN_STMT_KEYWORDS if kw in text)
    ops_hits = sum(1 for kw in OPS_STATS_KEYWORDS if kw in text)
    return (ops_hits >= MIN_KEYWORD_HITS, fin_hits >= MIN_KEYWORD_HITS)


def doc_role(has_ops: bool, has_fin: bool, is_annual: bool) -> str:
    prefix = "annual_" if is_annual else ""
    if has_ops and has_fin:
        return prefix + "combined_release"
    if has_fin:
        return prefix + "financial_statements"
    if has_ops:
        return prefix + "operating_stats"
    return prefix + "other"


# --------------------------------------------------------------------------
# Period inference
# --------------------------------------------------------------------------

_QUARTER_ENDS = {(3, 31): 1, (6, 30): 2, (9, 30): 3, (12, 31): 4}


def infer_period(report_date: str, filing_date: str) -> str:
    """Which fiscal quarter's RESULTS does this filing report?

    - FPI 6-K / Newmont 10-Q / 10-K / annual forms: reportDate is the actual
      period-end (quarter-end) and differs from filingDate -> bucket by
      reportDate's own calendar quarter.
    - Newmont 8-K: reportDate == filingDate (it's just "date of the
      announcement"), so we lag-map the filing month back to the quarter it
      is reporting on (Q4/FY released Jan-Mar, Q1 released Apr-Jun, Q2
      released Jul-Sep, Q3 released Oct-Dec).
    """
    fd = _parse_date(filing_date)
    rd = _parse_date(report_date) if report_date else None
    if rd is not None and rd != fd and (rd.month, rd.day) in _QUARTER_ENDS:
        q = _QUARTER_ENDS[(rd.month, rd.day)]
        return f"{rd.year}-Q{q}"
    return _lag_map(fd)


def _lag_map(fd: date) -> str:
    if fd.month in (1, 2, 3):
        return f"{fd.year - 1}-Q4"
    if fd.month in (4, 5, 6):
        return f"{fd.year}-Q1"
    if fd.month in (7, 8, 9):
        return f"{fd.year}-Q2"
    return f"{fd.year}-Q3"


def _parse_date(s: str) -> date:
    y, m, d = (int(x) for x in s.split("-"))
    return date(y, m, d)


# --------------------------------------------------------------------------
# Download + manifest
# --------------------------------------------------------------------------

def sha256_of_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_of_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def safe_local_name(period_hint: str, accession: str, filename: str) -> str:
    return f"{period_hint}_{accession}_{filename}"


def process_one_filing(company: Company, filing: dict) -> list[dict]:
    """Fetch a filing's index, download qualifying exhibits, return manifest
    rows (one per exhibit kept, downloaded-or-skipped either way)."""
    cik = filing["cik"]
    accession = filing["accessionNumber"]
    form = filing["form"]
    is_annual = form in company.annual_forms
    period_hint = infer_period(filing["reportDate"], filing["filingDate"])

    try:
        docs = list_index_documents(cik, accession)
    except FetchError as e:
        logger.error(f"[{company.ticker}] index fetch failed for {accession}: {e}")
        return [
            {
                "ticker": company.ticker,
                "cik": cik,
                "form": form,
                "filing_date": filing["filingDate"],
                "report_date": filing["reportDate"],
                "period_hint": period_hint,
                "is_annual_form": is_annual,
                "accession": accession,
                "seq": "",
                "doc_type": "",
                "exhibit_filename": "",
                "local_path": "",
                "bytes": 0,
                "sha256": "",
                "has_operating_stats": False,
                "has_financial_statements": False,
                "doc_role": "ERROR_INDEX_FETCH",
                "status": f"error: {e}",
            }
        ]

    rows = []
    out_dir = os.path.join(RAW_DIR, company.ticker)
    os.makedirs(out_dir, exist_ok=True)

    for d in docs:
        ext = os.path.splitext(d["filename"])[1].lower()
        if ext not in KEEP_EXTENSIONS:
            continue
        if d["size"] < MIN_EXHIBIT_BYTES:
            continue
        is_primary_type = d["doc_type"].upper() == form.upper()
        is_ex99 = d["doc_type"].upper().startswith("EX-99")
        if not (is_primary_type or is_ex99):
            continue

        local_name = safe_local_name(period_hint, accession, d["filename"])
        local_path = os.path.join(out_dir, local_name)
        rel_path = os.path.relpath(local_path, REPO_ROOT)

        if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
            digest = sha256_of_file(local_path)
            with open(local_path, "rb") as f:
                raw = f.read()
            has_ops, has_fin = classify_content(raw, d["filename"])
            logger.info(f"[{company.ticker}] SKIP (exists) {local_name}")
            status = "skipped-existing"
        else:
            try:
                raw = http_get(d["url"])
            except FetchError as e:
                logger.error(f"[{company.ticker}] download failed {d['url']}: {e}")
                rows.append(
                    {
                        "ticker": company.ticker,
                        "cik": cik,
                        "form": form,
                        "filing_date": filing["filingDate"],
                        "report_date": filing["reportDate"],
                        "period_hint": period_hint,
                        "is_annual_form": is_annual,
                        "accession": accession,
                        "seq": d["seq"],
                        "doc_type": d["doc_type"],
                        "exhibit_filename": d["filename"],
                        "local_path": "",
                        "bytes": 0,
                        "sha256": "",
                        "has_operating_stats": False,
                        "has_financial_statements": False,
                        "doc_role": "ERROR_DOWNLOAD",
                        "status": f"error: {e}",
                    }
                )
                continue
            with open(local_path, "wb") as f:
                f.write(raw)
            digest = sha256_of_bytes(raw)
            has_ops, has_fin = classify_content(raw, d["filename"])
            logger.info(
                f"[{company.ticker}] DOWNLOAD {local_name} "
                f"({len(raw):,}B, ops={has_ops}, fin={has_fin})"
            )
            status = "downloaded"

        rows.append(
            {
                "ticker": company.ticker,
                "cik": cik,
                "form": form,
                "filing_date": filing["filingDate"],
                "report_date": filing["reportDate"],
                "period_hint": period_hint,
                "is_annual_form": is_annual,
                "accession": accession,
                "seq": d["seq"],
                "doc_type": d["doc_type"],
                "exhibit_filename": d["filename"],
                "local_path": rel_path,
                "bytes": os.path.getsize(local_path),
                "sha256": digest,
                "has_operating_stats": has_ops,
                "has_financial_statements": has_fin,
                "doc_role": doc_role(has_ops, has_fin, is_annual),
                "status": status,
            }
        )
    return rows


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------

def gather_filings(company: Company) -> list[dict]:
    wanted_forms = set(company.quarterly_forms) | set(company.annual_forms) | set(company.extra_forms)
    all_filings = []
    for cik in company.ciks:
        logger.info(f"[{company.ticker}] listing filings for CIK {cik} ...")
        rows = fetch_all_filings_for_cik(cik)
        n_before = len(rows)
        kept = []
        for r in rows:
            if r["form"] not in wanted_forms:
                continue
            fd = r["filingDate"]
            if not (START_DATE.isoformat() <= fd <= END_DATE.isoformat()):
                continue
            if r["form"] == "8-K" and "2.02" not in (r["items"] or ""):
                continue  # only earnings-related 8-Ks
            kept.append(r)
        logger.info(
            f"[{company.ticker}] CIK {cik}: {n_before} total filings -> "
            f"{len(kept)} in scope ({wanted_forms}, {START_DATE}..{END_DATE})"
        )
        all_filings.extend(kept)
    all_filings.sort(key=lambda r: r["filingDate"])
    return all_filings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", default=None, help="comma-separated subset, e.g. NEM,GOLD")
    ap.add_argument("--limit", type=int, default=None, help="cap filings per company (debug)")
    args = ap.parse_args()

    companies = COMPANIES
    if args.tickers:
        wanted = set(t.strip().upper() for t in args.tickers.split(","))
        companies = [c for c in companies if c.ticker in wanted]

    t0 = time.time()
    all_rows: list[dict] = []

    # Phase 1: list filings per company (cheap, sequential is fine)
    plan: list[tuple[Company, dict]] = []
    for company in companies:
        filings = gather_filings(company)
        if args.limit:
            filings = filings[: args.limit]
        for f in filings:
            plan.append((company, f))

    logger.info(f"Total filings to inspect across {len(companies)} companies: {len(plan)}")

    # Phase 2: process filings concurrently (index fetch + exhibit downloads),
    # bounded overall by the shared RateLimiter regardless of worker count.
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(process_one_filing, c, f): (c, f) for c, f in plan}
        done = 0
        for fut in concurrent.futures.as_completed(futures):
            c, f = futures[fut]
            try:
                rows = fut.result()
                all_rows.extend(rows)
            except Exception as e:
                logger.error(f"[{c.ticker}] UNCAUGHT error on {f['accessionNumber']}: {e}")
            done += 1
            if done % 25 == 0:
                logger.info(f"... {done}/{len(plan)} filings processed")

    # Write manifest
    all_rows.sort(key=lambda r: (r["ticker"], r["filing_date"], r["accession"], r["exhibit_filename"]))
    fieldnames = [
        "ticker", "cik", "form", "filing_date", "report_date", "period_hint",
        "is_annual_form", "accession", "seq", "doc_type", "exhibit_filename",
        "local_path", "bytes", "sha256", "has_operating_stats",
        "has_financial_statements", "doc_role", "status",
    ]
    with open(MANIFEST_PATH, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in all_rows:
            w.writerow(r)

    logger.info(f"Manifest written: {MANIFEST_PATH} ({len(all_rows)} rows)")
    logger.info(f"Elapsed: {time.time() - t0:.1f}s")

    write_coverage_matrix(all_rows, companies)


def quarter_range(start: str, end: str) -> list[str]:
    out = []
    y, q = int(start[:4]), int(start[6])
    ey, eq = int(end[:4]), int(end[6])
    while (y, q) <= (ey, eq):
        out.append(f"{y}-Q{q}")
        q += 1
        if q > 4:
            q = 1
            y += 1
    return out


def write_coverage_matrix(rows: list[dict], companies: list[Company]):
    quarters = quarter_range("2021-Q1", "2026-Q2")
    tickers = [c.ticker for c in companies]

    ops_present: dict[tuple[str, str], bool] = {}
    fin_present: dict[tuple[str, str], bool] = {}
    for r in rows:
        if r["status"] not in ("downloaded", "skipped-existing"):
            continue
        key = (r["ticker"], r["period_hint"])
        if r["has_operating_stats"] in (True, "True"):
            ops_present[key] = True
        if r["has_financial_statements"] in (True, "True"):
            fin_present[key] = True

    with open(COVERAGE_PATH, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ticker", "quarter", "has_operating_stats", "has_financial_statements", "usable"])
        for t in tickers:
            for q in quarters:
                a = ops_present.get((t, q), False)
                b = fin_present.get((t, q), False)
                w.writerow([t, q, a, b, a and b])

    logger.info(f"Coverage matrix written: {COVERAGE_PATH}")

    # Also print a human-readable matrix to stdout/log.
    print("\n=== COVERAGE MATRIX: operating-stats(a) / financial-statements(b) ===")
    header = "quarter  | " + " | ".join(f"{t:^11s}" for t in tickers)
    print(header)
    print("-" * len(header))
    for q in quarters:
        cells = []
        for t in tickers:
            a = "a" if ops_present.get((t, q), False) else "-"
            b = "b" if fin_present.get((t, q), False) else "-"
            cells.append(f"{a}{b}".center(11))
        print(f"{q:8s} | " + " | ".join(cells))

    missing = []
    for t in tickers:
        for q in quarters:
            a = ops_present.get((t, q), False)
            b = fin_present.get((t, q), False)
            if not a and not b:
                missing.append((t, q, "NO DOCS AT ALL"))
            elif a and not b:
                missing.append((t, q, "ops-stats only, NO financial statements -- NOT USABLE"))
            elif b and not a:
                missing.append((t, q, "financial statements only, no ops-stats checksum"))
    if missing:
        print("\n=== GAPS ===")
        for t, q, reason in missing:
            print(f"  {t} {q}: {reason}")
    else:
        print("\nNo gaps: every ticker has both operating-stats and financial-statements docs for every quarter.")


if __name__ == "__main__":
    main()
