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

import numpy as np
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
ANNUAL_CASH_TAX = {"NEM": {2013: 361, 2014: 187, 2015: 223, 2016: 85,
                           2021: 1534, 2022: 1122, 2023: 794}}
# FY2015 is carried at 223 as originally filed. The FY2016 10-K restates the
# continuing-operations comparative to 77 -- a difference that is the Batu Hijau
# discontinued-operations reclassification, not a correction. The rest of the
# 2015 row is on the as-filed basis, so the tax has to be too.

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
# The exclusion runs on GAIM itself, cross-sectionally, against the same quarter's
# industry median. The earlier rule trimmed on the AISC/price ratio, which turned
# out not to track what it was trimming: r(aisc_ratio, L1) is -0.89 in the bull
# window but only -0.54 in the 2013-2016 trough, because AISC charges sustaining
# capex while GAIM charges all of it, and growth capex peaked exactly in the
# trough. In 2013Q4 Newmont breached the AISC cap while posting the best GAIM of
# the quarter, so removing it pushed the aggregate DOWN. A rule whose effect on
# the published number has no reliable sign cannot be corrected for, only removed.
#
# Measuring the deviation against the same quarter's median is what makes this
# cycle-neutral: when the whole industry moves, the reference moves with it, so a
# sector-wide collapse excludes nobody. The old sector-distress guard had to bolt
# that property on; here it is structural.
GAIM_OUTLIER_K = 3.0

# The scale is estimated WITHIN each quarter, never pooled across the panel. That
# is not a detail: dispersion in the trough (MAD-sigma 9.83) is 1.77x the bull
# window's (5.55), so one pooled scale would have excluded 7.8% of trough
# observations against 1.1% of bull ones -- reintroducing exactly the
# trough-thinning the AISC rule was abandoned for, in a new disguise. Per-quarter
# scaling brings that ratio to 1.6% vs 2.3%.
GAIM_OUTLIER_MIN_PT = 5.0      # ...and the gap must also be this many points, so a
                               # quarter where the companies happen to bunch cannot
                               # exclude anyone on noise. Does not bind today; the
                               # tightest observed quarterly scale is 0.68pt.
GAIM_OUTLIER_MIN_PANEL = 4     # below this, no trimming at all -- an outlier is not
                               # identifiable in a panel of three, and pretending
                               # otherwise would mean the rule bites hardest in the
                               # earliest years, where coverage is thinnest.

# Kept as a REPORTED DIAGNOSTIC only -- it no longer excludes anything. The ratio
# is externally verifiable and worth showing, and the sector-distress condition
# still tells a reader that an industry-wide cost squeeze was under way.
AISC_RATIO_CAP = 0.80
SECTOR_DISTRESS_SHARE = 0.20
SECTOR_DISTRESS_MIN_N = 2

SMOOTH_WINDOW = 4       # trailing quarters averaged

# ...and at least this many of the window's quarters must actually survive the
# exclusion. Without a floor, a window whose other three quarters were excluded
# still reports an "average" -- one built from the single quarter in which the
# company was not in trouble. That is the exclusion rule feeding the smoother the
# survivors and the smoother publishing them under a four-quarter label. The cost
# of the floor is the first two quarters of every company; the cost of not having
# it falls entirely on troughs, which is where the series has to be right.
SMOOTH_MIN_PERIODS = 3
SMOOTH_MONTHS = 12          # the window, in months
SMOOTH_MIN_MONTHS = 9       # ...and the minimum real coverage inside it


# Periods per year, by reporting frequency. Gold Fields publishes financial
# statements half-yearly only -- every Q1 and Q3 release says so in as many words
# -- so its rows are 2021H1 / 2021H2, never split into quarters. The contract
# forbids splitting a half, and interpolating one would manufacture a quarterly
# cycle that was never reported.
PERIODS_PER_YEAR = {"Q": 4, "H": 2}
PERIOD_MONTHS = {"Q": 3, "H": 6}

# AngloGold is not one frequency or the other -- it reported half-yearly through
# 2022, quarterly in 2021Q1-Q2 and again from 2023. So frequency cannot be a
# property of a COMPANY; it is a property of a ROW. Everything below therefore
# works in months rather than in period counts, which is the only unit both
# frequencies share.


def period_freq(period):
    """'2021Q3' -> 'Q'; '2021H1' -> 'H'."""
    return "H" if "H" in str(period)[4:] else "Q"


def period_start_month(period):
    """First month of the period, 1-12. Q3 -> 7; H2 -> 7."""
    p, n = str(period), int(str(period)[5])
    return (n - 1) * 6 + 1 if period_freq(p) == "H" else (n - 1) * 3 + 1


def period_order(period):
    """Chronological sort key. Plain string sorting puts 2021H2 BEFORE 2021Q1,
    because 'H' < 'Q' in ASCII -- which silently reverses a company's own
    history in any window function that trusts the row order."""
    return int(str(period)[:4]) * 100 + period_start_month(period)


def load_company(path):
    ticker = path.stem.split("_")[0]
    d = pd.read_csv(path)
    d["ticker"], d["year"] = ticker, d.quarter.str[:4].astype(int)
    d["freq"] = d.quarter.map(period_freq)
    d["months"] = d.freq.map(PERIOD_MONTHS)
    d["_ord"] = d.quarter.map(period_order)
    d = d.sort_values("_ord").reset_index(drop=True)

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
    # ...but the convention is not stable over time, so it cannot be keyed on the
    # ticker alone. Kinross INCLUDES capitalised interest inside capex in 2013-2016
    # and EXCLUDES it in 2021-2026; applying the modern correction to the old rows
    # would double-count it. An extraction agent that knows this signals it on the
    # row, and the row wins over the per-company default -- data that describes its
    # own convention beats a rule that has to guess the era.
    if "capitalised_interest" in d:
        ci = d.capitalised_interest.fillna(0)
        already_in_capex = d["flags"].fillna("").str.contains("CAPINT_INCLUDED_IN_CAPEX")
        if ticker == "GOLD":
            d["net_interest"] = d.net_interest - ci          # remove the double count
            d["flags"] = d["flags"].fillna("") + ";CAPINT_DEDUPED"
        elif ticker == "KGC":
            add = ci.where(~already_in_capex, 0)             # fill the gap, once
            d["capex_total"] = d.capex_total + add
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
    basis = pd.Series("as published (by-product, per oz sold)", index=d.index)

    # The substitution has to be decided PER ROW, not per column. Newmont publishes
    # a by-product figure alongside its co-product headline from 2021 but not in
    # 2013-2016, and a column-level test (.any()) substituted the whole column --
    # blanking every pre-2017 row of the company that ran the deepest cost squeeze
    # in the sample. An observation that carries a published AISC must never fall
    # out of the comparison because a SECOND, preferred figure is missing; it falls
    # back to the headline and says so.
    if "published_aisc_byproduct" in d:
        bp = d.published_aisc_byproduct
        aisc = bp.where(bp.notna(), aisc)           # Newmont, Kinross: prefer by-product
        sub = bp.notna()
        basis = basis.where(~sub, "by-product column substituted for the published headline")
        fallback = (~sub) & d.published_aisc.notna()
        basis = basis.where(~fallback, "published headline used -- no by-product figure this period")
        if fallback.any():
            d.loc[fallback, "flags"] = d.loc[fallback, "flags"].fillna("") + ";AISC_BASIS_FALLBACK"

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
    """Mark company-quarters that are outliers IN GAIM, against their own quarter.

    Needs the full cross-section: whether a reading is anomalous or simply what
    the industry did that quarter is only answerable by looking at the others.
    """
    # Group on the period STRING, which already separates 2021Q1 from 2021H1 --
    # but assert it, because a half-yearly row silently landing in a quarterly
    # cross-section would be compared against a period of twice its length.
    assert panel.groupby("quarter").freq.nunique().max() <= 1, "mixed frequency in one period"
    med = panel.groupby("quarter").L1.transform("median")
    panel["L1_median_q"] = med
    panel["L1_dev"] = panel.L1 - med
    # Robust scale, per quarter. 1.4826 makes the MAD a consistent estimator of
    # sigma for normal data, so K reads as "sigmas" the way a reader expects.
    panel["L1_scale_q"] = panel.groupby("quarter").L1_dev.transform(
        lambda s: np.median(np.abs(s.dropna())) * 1.4826 if s.notna().any() else np.nan)
    panel["panel_n_q"] = panel.groupby("quarter").L1.transform("count")

    panel["is_outlier"] = (
        (panel.L1_dev.abs() > GAIM_OUTLIER_K * panel.L1_scale_q)
        & (panel.L1_dev.abs() > GAIM_OUTLIER_MIN_PT)
        & (panel.panel_n_q >= GAIM_OUTLIER_MIN_PANEL)
    ).fillna(False)

    # Diagnostics only -- these gate nothing now, but a reader still wants to see
    # when the industry as a whole was running costs against the gold price.
    panel["aisc_ratio"] = panel.aisc_comparable / panel.realised_price
    breach = panel.aisc_ratio > AISC_RATIO_CAP
    testable = panel.aisc_ratio.notna()
    n_testable = testable.groupby(panel.quarter).transform("sum")
    panel["sector_breach_n"] = breach.groupby(panel.quarter).transform("sum")
    panel["sector_testable_n"] = n_testable
    panel["sector_breach_share"] = (panel.sector_breach_n / n_testable).where(n_testable > 0, 0.0)
    panel["sector_distress"] = ((panel.sector_breach_share >= SECTOR_DISTRESS_SHARE)
                                & (panel.sector_breach_n >= SECTOR_DISTRESS_MIN_N))
    return panel


def add_smoothed(d):
    """Average what survives the exclusion, over a trailing window.

    L2_n records how many quarters actually went into each average, so a reader
    can see when a "four-quarter" figure rests on three.
    """
    d = d.sort_values("_ord")
    # The window is twelve MONTHS, weighted by how much of the year each period
    # covers -- not a fixed number of rows. Four rows is a year for a quarterly
    # filer and two years for a half-yearly one, and AngloGold is both inside a
    # single series. For a purely quarterly company this reduces exactly to the
    # old trailing four-quarter simple mean, since every period then weighs 3.
    vals = d.L1.where(~d.is_outlier).to_numpy()
    mons, ends = d.months.to_numpy(), d._ord.to_numpy()
    L2, L2_n, L2_m = [], [], []
    for i in range(len(d)):
        num = den = cov = n = 0.0
        for j in range(i, -1, -1):
            if cov + mons[j] > SMOOTH_MONTHS:
                break
            cov += mons[j]
            if not pd.isna(vals[j]):
                num += vals[j] * mons[j]; den += mons[j]; n += 1
        L2.append(num / den if den else float("nan"))
        L2_n.append(n)
        # den, not cov: months of REAL data behind the average. Counting the
        # window's span instead would let an average built from two surviving
        # quarters publish itself as a twelve-month figure -- which is the
        # survivor-smoothing this gate exists to stop.
        L2_m.append(den)
    d["L2"] = L2
    d["L2_n"], d["L2_months"] = L2_n, L2_m
    d.loc[d.L2_months < SMOOTH_MIN_MONTHS, "L2"] = float("nan")
    return d


def censoring_audit(panel):
    """One row per quarter recording what the exclusion rule did, and to whom.

    Published alongside the series so suppression is never silent: a reader can
    see how much of any given quarter was removed before believing its level.
    """
    rows = []
    for q, g in panel.groupby("quarter"):
        excluded = g[g.is_outlier]
        breached = g[g.aisc_ratio > AISC_RATIO_CAP]
        rows.append({
            "quarter": q, "companies_covered": len(g),
            "panel_n_scored": int(g.panel_n_q.iloc[0]) if g.panel_n_q.notna().any() else 0,
            "L1_median_q": round(g.L1_median_q.iloc[0], 2) if g.L1_median_q.notna().any() else None,
            "L1_scale_q": round(g.L1_scale_q.iloc[0], 2) if g.L1_scale_q.notna().any() else None,
            "companies_excluded": len(excluded),
            "excluded_tickers": ";".join(sorted(excluded.ticker)),
            "excluded_devs": ";".join(f"{t}{d:+.1f}" for t, d in
                                      zip(excluded.ticker, excluded.L1_dev)),
            "L1_kept": round(g.loc[~g.is_outlier, "L1"].mean(), 2) if (~g.is_outlier).any() else None,
            "L1_all": round(g.L1.mean(), 2),
            # diagnostic, no longer a gate
            "companies_breaching_aisc_cap": len(breached),
            "breaching_tickers": ";".join(sorted(breached.ticker)),
            "sector_distress_diagnostic": bool(g.sector_distress.iloc[0]),
        })
    return pd.DataFrame(rows).assign(
        _ord=lambda x: x.quarter.map(period_order)).sort_values("_ord").drop(columns="_ord")


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
            freq = "/".join(sorted(g.freq.unique()))
            rows.append({
                "ticker": d.ticker.iloc[0], "year": year, "periods": len(g),
                "freq": freq,
                "months": int(g.months.sum()),
                "complete": int(g.months.sum()) == 12,
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
    # Two patterns, because the filename has to state the frequency. Gold Fields
    # publishes financial statements half-yearly only; calling its file
    # "_quarterly" would bury that in a flag nobody reads.
    files = sorted(list(INTERIM.glob("*_quarterly.csv"))
                   + list(INTERIM.glob("*_halfyearly.csv"))
                   + list(INTERIM.glob("*_mixed.csv")))
    if not files:
        raise SystemExit("no extracted company files in data/interim/")

    panel = flag_outliers(pd.concat(load_company(p) for p in files))
    frames = [add_smoothed(g) for _, g in panel.groupby("ticker")]
    audit = censoring_audit(panel)

    cols = ["ticker", "quarter", "freq", "gold_revenue", "gold_oz_sold", "realised_price",
            "w_gold", "L0a", "L0b", "aisc_margin", "L1", "L2", "L2_n", "published_aisc",
            "aisc_comparable", "aisc_basis_note", "gold_cost_total", "total_revenue",
            "net_income_attributable", "impairment_charges",
            "aisc_ratio", "is_outlier", "L1_median_q", "L1_dev", "L1_scale_q",
            "panel_n_q", "L2_months", "months", "sector_distress", "sector_breach_share",
            "sector_breach_n", "sector_testable_n",
            "recon_residual_pct", "flags"]
    # Sort on the chronological key, NOT on the period string -- 'H' < 'Q' would
    # put 2021H2 ahead of 2021Q1 and hand every downstream consumer a series that
    # runs backwards through its own mixed-frequency years.
    out = (pd.concat(frames).sort_values(["ticker", "_ord"])
           .reindex(columns=cols))
    out.to_csv(FINAL / "margins.csv", index=False)
    annual = build_annual(frames)
    annual.to_csv(FINAL / "margins_annual.csv", index=False)
    audit.to_csv(FINAL / "censoring_audit.csv", index=False)
    out[out.is_outlier].to_csv(FINAL / "trimmed_observations.csv", index=False)

    print(f"companies: {sorted(out.ticker.unique())}   quarterly rows: {len(out)}   "
          f"annual rows: {len(annual)} ({(~annual.complete).sum()} partial)")
    n_ex = int(out.is_outlier.sum())
    n_sector = int(audit.sector_distress_diagnostic.sum())
    print(f"excluded observations: {n_ex} of {len(out)} "
          f"({n_ex / len(out) * 100:.1f}%)   "
          f"quarters flagged sector-wide distress (diagnostic only): {n_sector}")
    if n_ex:
        print(audit[audit.companies_excluded > 0][
            ["quarter", "panel_n_scored", "L1_median_q", "L1_scale_q",
             "excluded_devs", "L1_all", "L1_kept"]].to_string(index=False))
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
