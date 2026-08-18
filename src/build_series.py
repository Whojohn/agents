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


def add_trimmed(d):
    """Drop distressed quarters, then average what is left."""
    d["aisc_ratio"] = d.aisc_comparable / d.realised_price
    keep = d.aisc_ratio <= AISC_RATIO_CAP
    d["is_outlier"] = ~keep
    d["L2"] = d.L1.where(keep).rolling(SMOOTH_WINDOW, min_periods=1).mean()

    log = [{"ticker": d.ticker.iloc[0], "quarter": r.quarter, "L1_value": round(r.L1, 2),
            "aisc": round(r.aisc_comparable, 0), "realised_price": round(r.realised_price, 0),
            "aisc_ratio_pct": round(r.aisc_ratio * 100, 1)}
           for r in d.itertuples() if not keep.iloc[r.Index]]
    return d, log


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

    frames, trims = [], []
    for path in files:
        d, log = add_trimmed(load_company(path))
        frames.append(d)
        trims.extend(log)

    cols = ["ticker", "quarter", "gold_revenue", "gold_oz_sold", "realised_price",
            "w_gold", "L0a", "aisc_margin", "L1", "L2", "published_aisc",
            "aisc_comparable", "aisc_basis_note", "gold_cost_total", "total_revenue",
            "aisc_ratio", "is_outlier", "recon_residual_pct", "flags"]
    out = pd.concat(frames).reindex(columns=cols).sort_values(["ticker", "quarter"])
    out.to_csv(FINAL / "margins.csv", index=False)
    annual = build_annual(frames)
    annual.to_csv(FINAL / "margins_annual.csv", index=False)
    pd.DataFrame(trims).to_csv(FINAL / "trimmed_observations.csv", index=False)

    print(f"companies: {sorted(out.ticker.unique())}   quarterly rows: {len(out)}   "
          f"annual rows: {len(annual)} ({(~annual.complete).sum()} partial)")
    print(f"trimmed observations logged: {len(trims)}")
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
