#!/usr/bin/env python3
"""Build the three published margin layers from extracted quarterly line items.

L0a  as-reported gold-segment operating margin   (zero adjustment)
L1   GAIM, fully-loaded forward-computed margin  (no outlier treatment)
L2   L1 after a two-sided 15% trim               (median-biased smoothing)

Plus the AISC margin, carried as the industry-standard cross-check. The
L1-vs-AISC gap is the product: it quantifies what AISC leaves out.

Reads whatever data/interim/<TICKER>_quarterly.csv files exist, so it can be
re-run as more companies land. Writes data/final/margins.csv and
data/final/trimmed_observations.csv.
"""
import math
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

TRIM_FRACTION = 0.15
TRIM_WINDOW = 8


def trimmed_mean(values, frac=TRIM_FRACTION):
    """Two-sided trimmed mean: drop floor(n*frac) from each tail, average the rest.

    Returns the trimmed mean and the values that were dropped, so every exclusion
    stays inspectable. Trimming that cannot be audited is an assertion, not a method.
    """
    clean = [v for v in values if pd.notna(v)]
    if not clean:
        return float("nan"), []
    k = math.floor(len(clean) * frac)
    if k == 0:
        return sum(clean) / len(clean), []
    ordered = sorted(clean)
    kept, dropped = ordered[k:len(ordered) - k], ordered[:k] + ordered[len(ordered) - k:]
    return (sum(kept) / len(kept), dropped) if kept else (sum(clean) / len(clean), [])


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
    d["aisc_margin"] = (1 - d.published_aisc / d.realised_price) * 100
    d["gold_revenue"] = rev
    return d


def add_trimmed(d):
    """Rolling two-sided trim over TRIM_WINDOW quarters, per company."""
    l2, dropped_log = [], []
    for i in range(len(d)):
        window = d.L1.iloc[max(0, i - TRIM_WINDOW + 1):i + 1]
        value, dropped = trimmed_mean(window.tolist())
        l2.append(value)
        for v in dropped:
            src = d.iloc[max(0, i - TRIM_WINDOW + 1):i + 1]
            match = src[src.L1 == v]
            if len(match):
                dropped_log.append({
                    "ticker": d.ticker.iloc[0], "window_ending": d.quarter.iloc[i],
                    "trimmed_quarter": match.quarter.iloc[0], "L1_value": round(v, 2),
                })
    d["L2"] = l2
    return d, dropped_log


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
            "recon_residual_pct", "flags"]
    out = pd.concat(frames).reindex(columns=cols).sort_values(["ticker", "quarter"])
    out.to_csv(FINAL / "margins.csv", index=False)
    pd.DataFrame(trims).to_csv(FINAL / "trimmed_observations.csv", index=False)

    print(f"companies: {sorted(out.ticker.unique())}   rows: {len(out)}")
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
