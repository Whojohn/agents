#!/usr/bin/env python3
"""Build the three published margin layers from extracted quarterly line items.

L0a  as-reported gold-segment operating margin   (zero adjustment)
L1   GAIM, fully-loaded forward-computed margin  (no outlier treatment)
L2   L1 with distressed quarters dropped, then a trailing 4-quarter average.
     A quarter is distressed when its AISC eats more than 80% of the realised
     gold price -- see AISC_RATIO_CAP.

Plus the AISC margin, carried as the industry-standard cross-check. The
L1-vs-AISC gap is the product: it quantifies what AISC leaves out.

Reads whatever data/interim/<TICKER>_quarterly.csv files exist, so it can be
re-run as more companies land. Writes data/final/margins.csv and
data/final/trimmed_observations.csv.
"""
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
INTERIM, FINAL = ROOT / "data/interim", ROOT / "data/final"

# Group-level costs, allocated to the gold segment pro-rata on gold revenue share
# (METHODOLOGY 7). Site-level costs are already gold-only and are not allocated.
GROUP_COSTS = [
    "corporate_g_and_a", "exploration_expensed", "capex_total",
    "reclamation_accretion", "lease_payments", "net_interest", "cash_tax_paid",
]

# Revenue column feeding GAIM vs the one feeding realised price. They differ for
# Barrick alone: its cost stack is consolidated-only, so GAIM must sit on the
# consolidated basis, while realised price must stay attributable to match the
# basis of the published AISC it is compared against.
REVENUE_BASIS = {
    "GOLD": ("segment_revenue_gold_consolidated", "segment_revenue_gold"),
}
DEFAULT_BASIS = ("segment_revenue_gold", "segment_revenue_gold")

# Cash taxes paid are disclosed only annually before 2024 for Newmont. The audited
# full-year figures are allocated across that year's quarters pro-rata on gold
# revenue. This is a derivation from a published number, not an estimate, and it is
# flagged on every row it touches — without it those quarters carry no tax at all
# and GAIM reads several points too high.
ANNUAL_CASH_TAX = {"NEM": {2021: 1534, 2022: 1122, 2023: 794}}

# Cash-tax catch-up payments that the company itself attributes to a PRIOR year.
# Agnico's Q1 2026 release states plainly: "Total cash taxes paid in the first
# quarter of 2026 were $1.8 billion, which included a $1.3 billion payment for the
# remaining cash tax liability for 2025." Leaving it in 2026Q1 puts a 44%-of-revenue
# lump in one quarter and forces the smoother to discard a real observation to hide
# a pure timing artefact. Reallocating it to the year it was earned fixes the
# distortion at source instead. {ticker: [(paid_quarter, amount, accrual_year)]}
TAX_REALLOCATION = {"AEM": [("2026Q1", 1300.0, 2025)]}

# A company-quarter is dropped from the aggregate when its AISC eats more than this
# share of the realised gold price. The point is to stop one company's distressed
# year dragging the industry average down -- a miner running at a 90% cost ratio is
# not representative of the sector, it is in trouble. A flat economic threshold beats
# a statistical trim here: it never discards a real industry-wide move, and anyone
# can check whether a given quarter passes it.
AISC_RATIO_CAP = 0.80

# ...but only when the breach is IDIOSYNCRATIC. The exclusion exists to stop one
# company's bad year dragging the industry average down. When most of the covered
# companies breach the cap in the same quarter, the breach is not an outlier --
# it is the cycle, and dropping it would delete precisely the trough this series
# exists to show. 2013-2015 is the case that makes this concrete. So a quarter in
# which this share of covered companies breaches excludes nobody.
SECTOR_DISTRESS_SHARE = 0.50

SMOOTH_WINDOW = 4       # trailing quarters averaged


def load_company(path):
    ticker = path.stem.split("_")[0]
    d = pd.read_csv(path).sort_values("quarter").reset_index(drop=True)
    d["ticker"], d["year"] = ticker, d.quarter.str[:4].astype(int)

    for year, fy_total in ANNUAL_CASH_TAX.get(ticker, {}).items():
        gap = (d.year == year) & d.cash_tax_paid.isna()
        if gap.any():
            share = d.loc[gap, "segment_revenue_gold"] / d.loc[d.year == year, "segment_revenue_gold"].sum()
            d.loc[gap, "cash_tax_paid"] = fy_total * share
            d.loc[gap, "flags"] = d.loc[gap, "flags"].fillna("") + ";CASH_TAX_ALLOCATED_FROM_FY"

    for paid_q, amount, accrual_year in TAX_REALLOCATION.get(ticker, []):
        src = d.quarter == paid_q
        tgt = d.year == accrual_year
        if src.any() and tgt.any():
            d.loc[src, "cash_tax_paid"] -= amount
            share = d.loc[tgt, "segment_revenue_gold"] / d.loc[tgt, "segment_revenue_gold"].sum()
            d.loc[tgt, "cash_tax_paid"] += amount * share
            d.loc[src | tgt, "flags"] = d.loc[src | tgt, "flags"].fillna("") + ";TAX_REALLOCATED_TO_ACCRUAL_YEAR"

    # Capitalised interest is handled differently by each filer, so the correction
    # differs in sign. Newmont and Agnico already count it exactly once (their capex
    # includes it and their interest line is already net of it) and are left alone.
    #   Barrick  DOUBLE-COUNTS: capex includes capitalised interest AND net_interest
    #            is the gross interest expense, before the capitalisation credit.
    #   Kinross  OMITS it: it sits in a separate cash-flow investing line that feeds
    #            neither column.
    if "capitalised_interest" in d:
        ci = d.capitalised_interest.fillna(0)
        if ticker == "GOLD":
            d["net_interest"] = d.net_interest - ci          # remove the double count
            d["flags"] = d["flags"].fillna("") + ";CAPINT_DEDUPED"
        elif ticker == "KGC":
            d["capex_total"] = d.capex_total + ci            # fill the gap
            d["flags"] = d["flags"].fillna("") + ";CAPINT_ADDED"

    gaim_col, price_col = REVENUE_BASIS.get(ticker, DEFAULT_BASIS)
    rev = d[gaim_col]
    royalties = d.royalties.fillna(0) if "royalties" in d else 0

    # Gold share of total revenue, the allocation weight for group-level costs.
    d["w_gold"] = (rev / d.total_revenue).clip(0, 1)
    site_cost = d.opcost_ex_dda.fillna(0) + royalties
    group_cost = d.reindex(columns=GROUP_COSTS).fillna(0).sum(axis=1) * d.w_gold

    # L0a deducts DD&A (an accounting margin); L1 deducts total capex instead
    # (a cash-economics margin). Never both -- that double-counts the same capital.
    d["L0a"] = (rev - site_cost - d.segment_dda.fillna(0)) / rev * 100
    d["L1"] = (rev - site_cost - group_cost) / rev * 100

    # L0b -- company-level net margin, straight off the income statement. This is
    # the ONLY published layer that carries impairments, and in 2013-2015 the
    # impairments ARE the story: a deeply negative L0b is the correct reading of
    # those years, not a data error. GAIM deliberately excludes them (it charges
    # total capex, so adding a non-cash write-down of past capex would charge the
    # same capital twice) -- which is exactly why the accounting layer has to be
    # published alongside it rather than dropped.
    if "net_income_attributable" in d:
        d["L0b"] = d.net_income_attributable / d.total_revenue * 100
    d["realised_price"] = d[price_col] / d.gold_oz_sold * 1e6

    # Put every company's AISC on ONE basis before comparing: by-product, per gold
    # ounce SOLD. Companies publish four different conventions -- Newmont headlines
    # co-product, Kinross headlines gold-equivalent, Agnico denominates per ounce
    # PRODUCED -- and comparing them unconverted makes a presentation choice look
    # like an economic difference.
    aisc = d.published_aisc.copy()
    basis = "as published (by-product, per oz sold)"
    if "published_aisc_byproduct" in d and d.published_aisc_byproduct.notna().any():
        aisc = d.published_aisc_byproduct           # Newmont (co-product headline), Kinross (GEO headline)
        basis = "by-product column substituted for the published headline"
    if "aisc_denominator_oz" in d and d.aisc_denominator_oz.notna().any() \
            and str(d.aisc_basis.iloc[0]).lower().startswith("by-product"):
        # Agnico: restate per-ounce-produced onto an ounces-sold denominator
        aisc = aisc * d.aisc_denominator_oz / d.gold_oz_sold
        basis = "restated from per-ounce-produced to per-ounce-sold"
    d["aisc_comparable"], d["aisc_basis_note"] = aisc, basis
    d["aisc_margin"] = (1 - aisc / d.realised_price) * 100
    d["gold_revenue"] = rev
    d["gold_cost_total"] = site_cost + group_cost   # lets the page re-aggregate any subset
    return d


def flag_outliers(panel):
    """Mark distressed company-quarters -- unless the whole sector is distressed.

    Needs the full cross-section, because whether a breach is an outlier or the
    cycle is only answerable by looking at what the other companies did in the
    same quarter. See SECTOR_DISTRESS_SHARE.
    """
    panel["aisc_ratio"] = panel.aisc_comparable / panel.realised_price
    breach = panel.aisc_ratio > AISC_RATIO_CAP
    panel["sector_breach_share"] = breach.groupby(panel.quarter).transform("mean")
    panel["sector_distress"] = panel.sector_breach_share >= SECTOR_DISTRESS_SHARE
    panel["is_outlier"] = breach & ~panel.sector_distress
    return panel


def add_smoothed(d):
    """Average what survives the exclusion, over a trailing window."""
    d = d.sort_values("quarter")
    d["L2"] = d.L1.where(~d.is_outlier).rolling(SMOOTH_WINDOW, min_periods=1).mean()
    return d


def censoring_audit(panel):
    """One row per quarter recording what the exclusion rule did, and to whom.

    Published alongside the series so suppression is never silent: a reader can
    see how much of any given quarter was removed before believing its level.
    """
    rows = []
    for q, g in panel.groupby("quarter"):
        breached = g[g.aisc_ratio > AISC_RATIO_CAP]
        excluded = g[g.is_outlier]
        rows.append({
            "quarter": q, "companies_covered": len(g),
            "companies_breaching_cap": len(breached),
            "breach_share_pct": round(g.sector_breach_share.iloc[0] * 100, 1),
            "sector_distress": bool(g.sector_distress.iloc[0]),
            "companies_excluded": len(excluded),
            "excluded_tickers": ";".join(sorted(excluded.ticker)),
            "breaching_tickers": ";".join(sorted(breached.ticker)),
            "L1_kept": round(g.loc[~g.is_outlier, "L1"].mean(), 2) if (~g.is_outlier).any() else None,
            "L1_all": round(g.L1.mean(), 2),
        })
    return pd.DataFrame(rows)


def build_annual(frames):
    """Annual series: sum the dollar line items first, then form the ratio.

    Averaging four quarterly ratios would weight a small quarter equally with a
    large one. Summing the components and dividing once is the only correct way.
    """
    rows = []
    for d in frames:
        gaim_col, price_col = REVENUE_BASIS.get(d.ticker.iloc[0], DEFAULT_BASIS)
        for year, g in d.groupby("year"):
            rev, price_rev = g[gaim_col].sum(), g[price_col].sum()
            oz = g.gold_oz_sold.sum()
            royalties = g.royalties.fillna(0).sum() if "royalties" in g else 0
            site = g.opcost_ex_dda.fillna(0).sum() + royalties
            w = min(rev / g.total_revenue.sum(), 1.0)
            group_cost = g.reindex(columns=GROUP_COSTS).fillna(0).sum().sum() * w
            # ounce-weighted AISC: total AISC dollars over total ounces
            aisc_usd = (g.aisc_comparable * g.gold_oz_sold).sum() / 1e6
            rows.append({
                "ticker": d.ticker.iloc[0], "year": year, "quarters": len(g),
                "complete": len(g) == 4,
                "gold_revenue": round(rev, 1), "gold_oz_sold": int(oz),
                "realised_price": round(price_rev / oz * 1e6, 0),
                "L0a": round((rev - site - g.segment_dda.fillna(0).sum()) / rev * 100, 2),
                "L1": round((rev - site - group_cost) / rev * 100, 2),
                "aisc_margin": round((1 - aisc_usd / price_rev) * 100, 2),
                "aisc_weighted": round(aisc_usd * 1e6 / oz, 0),
            })
    return pd.DataFrame(rows)


def main():
    FINAL.mkdir(parents=True, exist_ok=True)
    files = sorted(INTERIM.glob("*_quarterly.csv"))
    if not files:
        raise SystemExit("no extracted company files in data/interim/")

    panel = flag_outliers(pd.concat(load_company(p) for p in files))
    frames = [add_smoothed(g) for _, g in panel.groupby("ticker")]
    audit = censoring_audit(panel)

    cols = ["ticker", "quarter", "gold_revenue", "gold_oz_sold", "realised_price",
            "w_gold", "L0a", "L0b", "aisc_margin", "L1", "L2", "published_aisc",
            "aisc_comparable", "aisc_basis_note", "gold_cost_total", "total_revenue",
            "aisc_ratio", "is_outlier", "sector_distress", "sector_breach_share",
            "recon_residual_pct", "flags"]
    out = pd.concat(frames).reindex(columns=cols).sort_values(["ticker", "quarter"])
    out.to_csv(FINAL / "margins.csv", index=False)
    annual = build_annual(frames)
    annual.to_csv(FINAL / "margins_annual.csv", index=False)
    audit.to_csv(FINAL / "censoring_audit.csv", index=False)
    out[out.is_outlier].to_csv(FINAL / "trimmed_observations.csv", index=False)

    print(f"companies: {sorted(out.ticker.unique())}   quarterly rows: {len(out)}   "
          f"annual rows: {len(annual)} ({(~annual.complete).sum()} partial)")
    n_sector = int(audit.sector_distress.sum())
    print(f"excluded observations: {int(out.is_outlier.sum())}   "
          f"quarters shielded as sector-wide distress: {n_sector}")
    if n_sector:
        print(audit[audit.sector_distress][
            ["quarter", "companies_breaching_cap", "companies_covered",
             "L1_all", "L1_kept"]].to_string(index=False))
    for t, g in out.groupby("ticker"):
        print(f"  {t:5} L0a {g.L0a.mean():5.1f}%  AISC {g.aisc_margin.mean():5.1f}%  "
              f"GAIM {g.L1.mean():5.1f}%  gap {(g.aisc_margin - g.L1).mean():5.1f}pt")

    violations = out[out.aisc_margin <= out.L1]
    print(f"\ninvariant AISC margin > GAIM: {'HOLDS' if violations.empty else 'VIOLATED'}"
          f" ({len(violations)} exceptions)")
    if not violations.empty:
        print(violations[["ticker", "quarter", "aisc_margin", "L1"]].to_string(index=False))


if __name__ == "__main__":
    main()
