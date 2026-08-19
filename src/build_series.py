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

import re

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
INTERIM, FINAL = ROOT / "data/interim", ROOT / "data/final"

# Group-level costs, allocated to the gold segment pro-rata on gold revenue share
# (METHODOLOGY 7). Site-level costs are already gold-only and are not allocated.
# care_and_maintenance: the operating cost of IDLED capacity -- COVID
# suspensions in 2020, but also Obuasi from 2014 and any mine on standby. It is
# a real cash cost of the gold business that no field previously captured, and
# Newmont's own AISC folds it in while our opcost_ex_dda (costs-applicable-to-
# sales only) does not. Omitting it overstated Newmont's 2020Q2 GAIM by 5.29
# points. It is NOT a one-off item: it recurs for as long as the idling lasts.
GROUP_COSTS = [
    "corporate_g_and_a", "exploration_expensed", "capex_total",
    "reclamation_accretion", "lease_payments", "net_interest", "cash_tax_paid",
    "care_and_maintenance",
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
                           2017: 214, 2018: 429, 2019: 437, 2020: 400,
                           2021: 1534, 2022: 1122, 2023: 794}}
# 2017-2020 read off the 10-K supplemental cash-flow disclosure "Income and
# mining taxes paid, net of refunds". Each 10-K prints three years, so every
# figure below is confirmed by two or three separate filings: 214 appears in
# the FY2017, FY2018 and FY2019 10-Ks; 429 in FY2018/2019/2020; 437 in
# FY2019/2020. Newmont discloses no interim cash-tax figure at all -- not
# quarterly, not cumulative -- so there is no subtraction path and the annual
# total is pro-rated on gold revenue (Tier C, error centred on zero). Without
# these four years the 2017-2020 rows carried a Tier D zero-fill worth 3.44
# points of overstated margin apiece, which graded all 16 of them unpublishable.
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
PERIOD_MONTHS = {"Q": 3, "H": 6, "A": 12}

# AngloGold is not one frequency or the other -- it reported half-yearly through
# 2022, quarterly in 2021Q1-Q2 and again from 2023. So frequency cannot be a
# property of a COMPANY; it is a property of a ROW. Everything below therefore
# works in months rather than in period counts, which is the only unit both
# frequencies share.


def period_freq(period):
    """'2021Q3' -> 'Q'; '2021H1' -> 'H'; '2005FY' -> 'A'.

    'A' exists because Kinross filed NOTHING interim in 2005 -- no quarter of
    that year is recoverable, and the only figures that exist are the audited
    annual ones in the FY2006 40-F. Splitting them into four quarters is the
    pro-rata the methodology forbids, so the year is carried as one 12-month
    observation instead. Before this, period_freq read '2005FY' as 'Q' (there
    is no 'H' in 'FY') and period_start_month then died on int('Y') -- loudly,
    which is the one good thing about it.
    """
    tail = str(period)[4:]
    if tail.upper().startswith(("FY", "A")):
        return "A"
    return "H" if "H" in tail else "Q"


def period_start_month(period):
    """First month of the period, 1-12. Q3 -> 7; H2 -> 7; FY -> 1."""
    p = str(period)
    f = period_freq(p)
    if f == "A":
        return 1
    n = int(p[5])
    return (n - 1) * 6 + 1 if f == "H" else (n - 1) * 3 + 1


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
        # ...and the same margin with non-recurring items taken back out. A
        # deconsolidation gain is not gold-mining income: Newmont's 2019Q3 net
        # income of $2,178m is dominated by a $2,366m gain on forming the
        # Nevada Gold Mines JV, which prints an 80.3% "margin" for a quarter
        # that earned nothing of the sort. Newmont strips it in its own
        # non-GAAP reconciliation, as (2,366). This column is null wherever
        # nobody has looked for such items yet -- absence here means unchecked,
        # not clean, so L0b_adj falls back to L0b rather than asserting zero.
        nonrec = (d.l0b_nonrecurring.fillna(0) if "l0b_nonrecurring" in d else 0)
        d["L0b_adj"] = (d.net_income_attributable - nonrec) / d.total_revenue * 100
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

    # Restate a per-ounce-PRODUCED AISC onto an ounces-SOLD denominator, so it
    # can be compared with a realised price that is revenue over ounces sold.
    #
    # This was decided per COLUMN and off the first row: it required
    # aisc_basis.iloc[0] to start with "by-product". Agnico's first row is
    # 2013Q1, whose basis string begins "single measure (pre-WGC AEM
    # methodology), per ounce PRODUCED" -- so the test was False and the
    # restatement never ran for ANY Agnico row, including the 2021+ rows whose
    # basis does begin with "by-product". Every Agnico row then went out
    # labelled "as published (by-product, per oz sold)", which is not true of a
    # single one of them.
    #
    # The condition was also asking the wrong question. by-product vs
    # co-product is about how BY-PRODUCT REVENUE is treated; produced vs sold
    # is about the OUNCE DENOMINATOR. They are independent, and only the second
    # one is what this restatement corrects.
    if "aisc_denominator_oz" in d:
        den = d.aisc_denominator_oz
        per_produced = d.aisc_basis.astype(str).str.contains("produced", case=False, na=False)
        do = per_produced & den.notna() & d.gold_oz_sold.notna() & aisc.notna()
        aisc = aisc.where(~do, aisc * den / d.gold_oz_sold)
        basis = basis.where(~do, "restated from per-ounce-produced to per-ounce-sold")
        unfixed = per_produced & ~do
        if unfixed.any():
            d.loc[unfixed, "flags"] = (d.loc[unfixed, "flags"].fillna("")
                                       + ";AISC_PER_PRODUCED_NOT_RESTATED")
    # Recompute the AISC reconstruction residual instead of trusting the stored
    # column. That column mixes units: some agents wrote a fraction (-0.009 for
    # -0.9%), some wrote percent (1.667 for +1.67%), and NEM_quarterly.csv
    # manages BOTH inside one column -- 0.0001 in 2017Q1 against 0.208 in
    # 2025Q4. The contract's own admissibility gate is "ties within 2%", and it
    # has never been enforced anywhere, because nothing could read the column it
    # depends on. Derived here from the two figures themselves, so the gate is
    # evaluable and the units are one thing.
    if "recon_aisc" in d:
        # Which published figure the reconstruction was built against is a
        # property of the extraction, not of the company, so it is read per row
        # rather than assumed. Gold Fields reconciles to AIC because its
        # capex_total is TOTAL capex -- AIC's scope -- while AISC counts
        # sustaining capex only. Scoring it against AISC reports 9.4% where the
        # real residual is 5.1%, and would trip the gate on a basis mismatch
        # that is not an extraction error. Defaulting to AISC keeps every
        # existing row's meaning unchanged.
        basis_col = (d.recon_basis.astype(str).str.upper() if "recon_basis" in d
                     else pd.Series("AISC", index=d.index))
        ref = d.published_aisc.where(basis_col != "AIC",
                                     d.published_aic if "published_aic" in d else d.published_aisc)
        d["recon_basis_used"] = basis_col.where(ref.notna(), None)
        d["recon_residual_calc"] = (d.recon_aisc - ref) / ref * 100
        # The contract makes an observation admissible only if the reconstruction
        # ties within 2% or NO_AISC_CHECK is set with a reason. Mark the failures
        # mechanically so they cannot pass unremarked: WHY a given row misses is
        # in the extraction's own flags (Barrick's, for instance, is a
        # consolidated cost stack over an attributable ounce count), but THAT it
        # misses should not depend on a reader noticing.
        miss = d.recon_residual_calc.abs() > 2.0
        if miss.any():
            d.loc[miss, "flags"] = d.loc[miss, "flags"].fillna("") + ";CHECKSUM_OUTSIDE_GATE"
    d["aisc_comparable"], d["aisc_basis_note"] = aisc, basis
    d["aisc_margin"] = (1 - aisc / d.realised_price) * 100

    # AngloGold's published AISC is denominated on ATTRIBUTABLE ounces including
    # equity-accounted joint ventures; our gold revenue is CONSOLIDATED and
    # excludes them. Source, 2014-Q4 6-K (d878132d6k.htm): income statement
    # "Gold income 1,278" with the segment note "Equity-accounted investments
    # included above (142)", against the AISC appendix's "Attributable gold
    # income including realised non-hedge derivatives 1,407" over "Attributable
    # gold sold - oz (000) 1,171". 1,278/1.171m = $1,091 against the company's
    # own "Price received per unit" of $1,202.
    #
    # So aisc_margin = 1 - AISC/price divides an attributable AISC by a
    # consolidated price and understates the margin by 4.9 to 23.8 points. The
    # right denominator -- attributable gold income -- is disclosed but not yet
    # extracted, so the column is WITHHELD rather than published wrong. Ends at
    # 2023Q1, where AngloGold's own basis change makes the two agree (2025Q1:
    # 1,927/670k = $2,876 against a published $2,875).
    #
    # This also explains the panel's only "AISC margin > GAIM" violation, AU
    # 2016H2: not rounding noise, an artefact of the understated price.
    if d.ticker.iloc[0] == "AU":
        bad = d._ord < period_order("2023Q1")
        if bad.any():
            d.loc[bad, "aisc_margin"] = pd.NA
            d.loc[bad, "flags"] = (d.loc[bad, "flags"].fillna("")
                + ";AISC_MARGIN_WITHHELD:PRICE_BASIS_MISMATCH_CONSOL_REV_VS_ATTRIB_OZ")
    d["gold_revenue"] = rev
    d["gold_cost_total"] = site_cost + group_cost   # lets the page re-aggregate any subset
    return d


def flag_outliers(panel):
    """Mark company-quarters that are outliers IN GAIM, against their own quarter.

    Needs the full cross-section: whether a reading is anomalous or simply what
    the industry did that quarter is only answerable by looking at the others.
    """
    # Group on the period STRING, which already separates 2021Q1 from 2021H1.
    # The old guard here asserted that each period holds one freq -- but freq is
    # DERIVED from the period string, so it could never fail and protected
    # nothing. The failure it was reaching for is a row whose label says one
    # length and whose months column says another, which is a real thing an
    # extraction agent can produce. Check that instead.
    bad = panel[panel.months != panel.quarter.map(period_freq).map(PERIOD_MONTHS)]
    assert bad.empty, ("period label disagrees with months column: "
                       + str(bad[["ticker", "quarter", "months"]].to_dict("records")[:5]))
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

    # ---- half-year rows are tested at half-year frequency -------------------
    # Only Gold Fields and AngloGold file twice a year, so a half-year period
    # holds one or two companies -- always below GAIM_OUTLIER_MIN_PANEL. Every
    # one of the 33 half-year observations was therefore STRUCTURALLY exempt
    # from trimming while 14 of 256 quarterly rows were excluded, and the
    # exemption landed precisely on the two companies with the worst fidelity
    # grades. 2005-2012 makes it worse: Gold Fields files half-yearly for the
    # whole span.
    #
    # The fix is not to lower the floor -- an outlier genuinely is not
    # identifiable in a panel of two. It is to give those rows a real
    # cross-section by folding each quarterly filer's two quarters into one
    # half-year figure. Aggregating quarters INTO a half is allowed; it is
    # SPLITTING a half into quarters that the methodology forbids. Every
    # observation is then judged against a panel built at its own frequency.
    # Annual rows get no half. A 12-month figure placed in a 6-month bucket is
    # the split we refused to make when extracting it.
    ann = panel.freq == "A"
    panel["_half"] = np.where(
        ann, "",
        panel.quarter.str[:4] + "H"
        + np.where(panel.quarter.str[4] == "H", panel.quarter.str[5],
                   np.where(panel.quarter.str[5].where(~ann, "1").astype(int) <= 2, "1", "2")))
    fold = (panel.assign(_rw=panel.L1 * panel.gold_revenue)
                 .groupby(["_half", "ticker"])
                 .agg(_rw=("_rw", "sum"), _rev=("gold_revenue", "sum"),
                      _mon=("months", "sum"), _n=("L1", "count")))
    # A company enters the half-year cross-section only if it actually covers
    # the whole half. A single reported quarter is not a half-year observation.
    fold = fold[(fold._mon == 6) & (fold._n > 0) & (fold.index.get_level_values("_half") != "")]
    fold["_g"] = fold._rw / fold._rev
    grp = fold.groupby("_half")._g
    hstat = pd.DataFrame({
        "_hmed": grp.transform("median"),
        "_hn": grp.transform("count"),
    })
    hstat["_hdev"] = fold._g - hstat._hmed
    hstat["_hscale"] = hstat.groupby(level=0)._hdev.transform(
        lambda x: np.median(np.abs(x.dropna())) * 1.4826 if x.notna().any() else np.nan)

    isH = panel.freq == "H"
    if isH.any():
        key = pd.MultiIndex.from_arrays([panel.loc[isH, "_half"], panel.loc[isH, "ticker"]])
        for col, src in (("L1_median_q", "_hmed"), ("L1_scale_q", "_hscale"),
                         ("panel_n_q", "_hn")):
            panel.loc[isH, col] = hstat[src].reindex(key).to_numpy()
        panel.loc[isH, "L1_dev"] = panel.loc[isH, "L1"] - panel.loc[isH, "L1_median_q"]
        panel.loc[isH, "is_outlier"] = (
            (panel.loc[isH, "L1_dev"].abs() > GAIM_OUTLIER_K * panel.loc[isH, "L1_scale_q"])
            & (panel.loc[isH, "L1_dev"].abs() > GAIM_OUTLIER_MIN_PT)
            & (panel.loc[isH, "panel_n_q"] >= GAIM_OUTLIER_MIN_PANEL)
        ).fillna(False)
    panel = panel.drop(columns=["_half"])

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


# ---------------------------------------------------------------------------
# Fidelity grading (DEGRADATION.md section 9)
# ---------------------------------------------------------------------------
# Twelve positions, fixed order, one character each: A / E (A-equivalent) /
# B / C / D. The vector is the honest statement of how each row was built;
# the composite grade is a summary of it, and the bias columns are what the
# non-A positions are worth in GAIM percentage points.
FIDELITY_FIELDS = [
    "segment_revenue_gold", "total_revenue", "opcost_ex_dda", "royalties",
    "corporate_g_and_a", "exploration_expensed", "capex_total",
    "reclamation_accretion", "lease_payments", "net_interest",
    "cash_tax_paid", "one_off_items", "care_and_maintenance",
]

# Cost share of gold revenue, in GAIM points, at two MEASURED price anchors.
#   (bull_center, bull_p90, trough_center, trough_p90)
# bull   = 2021Q1-2026Q2, ounce-weighted realised price $2,494 (n=88)
# trough = 2013Q1-2016Q4, ounce-weighted realised price $1,267 (n=64)
#
# Two anchors, not one anchor plus an elasticity. DEGRADATION section 1.3
# projected the trough from the bull window with a constant-elasticity price
# factor; section 1.4 tested that projection against the trough once it was
# extracted and found it over-predicts eight of ten line items and flips the
# sign of aggregate GAIM (-6.9% predicted against +12.5% measured), because a
# purely mechanical price model has no term for managements cutting capex and
# exploration -- the two lines whose measured elasticity came in at ~0.
# Interpolating between two measured points cannot make that mistake.
BIAS_ANCHOR = {
    "opcost_ex_dda":         (41.67, 53.17, 51.82, 61.50),
    "royalties":             ( 3.75,  4.95,  2.47,  2.75),
    "corporate_g_and_a":     ( 2.01,  3.50,  3.62,  5.92),
    "exploration_expensed":  ( 2.92,  4.52,  3.01,  6.09),
    "capex_total":           (20.92, 28.25, 19.93, 33.30),
    "reclamation_accretion": ( 0.81,  1.78,  0.97,  1.35),
    "lease_payments":        ( 0.33,  0.72,  0.77,  1.53),
    "net_interest":          ( 1.08,  2.23,  3.11,  8.24),
    "cash_tax_paid":         ( 6.70, 16.21,  3.44,  7.96),
    # Losing the split makes w_gold := 1, which UNDERSTATES cost and so
    # overstates GAIM; sign handled with the others, magnitude per 9.4.
    "total_revenue":         ( 2.83,  2.83,  2.83,  2.83),
}
ANCHOR_P_BULL, ANCHOR_P_TROUGH = 2494.0, 1267.0

# Legacy flags predate the TIER* vocabulary. A bare NOT_DISCLOSED grades D --
# a silent zero-fill -- EXCEPT for the (company, field) pairs section 1.1
# verified as bundled into a line already being counted, which are the
# original A-equivalent precedent. Anything not on this list stays D, so the
# unmodernised flags show up as work to do rather than being assumed away.
LEGACY_A_EQUIVALENT = {
    ("AEM", "royalties"), ("KGC", "royalties"), ("NEM", "royalties"),
    ("AEM", "reclamation_accretion"),
    # AU proven by experiment, not assumed. This list was built from
    # DEGRADATION 1.1, which only ever assessed four companies, so AngloGold
    # and Gold Fields defaulted to Tier D -- a silent zero-fill -- on a blank
    # royalties line. That produced a headline claim that AngloGold's blanks
    # were worth 3.9 to 4.6 points of overstated margin, the largest single
    # defect in the panel. They were worth nothing. Extracting the real
    # royalty figures for eight periods and subtracting them out of
    # opcost_ex_dda moved GAIM on exactly ZERO rows, which is only possible if
    # the royalties were already inside opcost. The blank was presentational.
    # Gold Fields needs no entry: it populates royalties on all 32 rows.
    ("AU", "royalties"), ("AU", "reclamation_accretion"),
}

# Some gaps are properties of the accounting standard, not of the filer, and
# they are A-equivalent everywhere at once: the cost was real but sat inside a
# line already being counted, so entering nothing loses nothing. Keyed by the
# first year the separate line is required to exist.
#   lease_payments: IFRS 16 and ASC 842 both bind from 2019-01-01. Before that
#     operating leases were an expense inside operating costs -- which the
#     build already deducts -- so a null is exact, not a zero-fill.
#   reclamation_accretion: SFAS 143 from FY2003, before the panel starts.
STANDARD_ERA_AEQ = {"lease_payments": 2019, "reclamation_accretion": 2003}

# one_off_items does not exist as a column for ANY company in ANY period
# (section 3.12). It is a whole-domain unquantified wedge, and the spec is
# internally inconsistent about what that does: 9.3 says a D anywhere forces
# grade D, while 3.12 and 11 say it CAPS the grade at C. Those cannot both
# hold. Resolved here in favour of the cap: max(tier) is taken over the
# eleven quantified positions, and position 12 sets the C ceiling. Reading it
# the other way would pin literally every row in the panel to D and make the
# composite grade constant -- a grade that never varies cannot expose a
# fidelity difference, which is the only reason 9.5 puts it on the chart.
# Both of these are known cost categories whose COVERAGE is unverified rather
# than known-absent. A blank care_and_maintenance usually means no mine was
# idled that quarter -- exact, not a gap -- but nobody has checked per company,
# so it caps the grade at C instead of flooring it at D. A row that actually
# carries the number grades A on that position, which is how the cap clears.
UNQUANTIFIED_FIELDS = {"one_off_items", "care_and_maintenance"}

TIER_RE = re.compile(r"TIER(AEQ|A|B|C|D):([a-z_]+)(?::([A-Za-z0-9_]+))?")
TIER_ORDER = {"A": 0, "E": 0, "B": 1, "C": 2, "D": 3}

BUDGET_CAP, BUDGET_FLOOR = 2.5, 1.0


def _anchor_at(field, price):
    """Cost share for `field` at `price`, log-interpolated between two MEASURED
    anchors. Outside [trough, bull] the value is clamped and the caller marks
    the row unquantified -- section 1.4.4 forbids extrapolating the factor
    below $1,267, and the 2005-2012 era ($450-1,670) sits partly under it."""
    b_c, b_p90, t_c, t_p90 = BIAS_ANCHOR[field]
    if not price or pd.isna(price):
        return t_c, t_p90, True
    p = float(price)
    outside = not (ANCHOR_P_TROUGH <= p <= ANCHOR_P_BULL)
    p = min(max(p, ANCHOR_P_TROUGH), ANCHOR_P_BULL)
    if b_c <= 0 or t_c <= 0:
        return t_c, t_p90, outside
    w = np.log(p / ANCHOR_P_TROUGH) / np.log(ANCHOR_P_BULL / ANCHOR_P_TROUGH)
    return (t_c * (b_c / t_c) ** w, t_p90 * (b_p90 / t_p90) ** w, outside)


# Descriptive flags that DESCRIBE a Tier-C substitution but were written
# WITHOUT their machine-read partner. EXTRACTION_CONTRACT section C.2 is
# explicit that both must be written; 76 rows across two companies wrote
# only the descriptive half. The grader sees a non-null value and nothing
# telling it otherwise, so it graded every one of them Tier A.
#
# The visible damage was not the grade -- it was the band. Tier C appeared
# ZERO times in 3,757 vector positions, and because Tier C is the only tier
# that moves the LOWER edge (A/E/B/D all push one way), bias_pt_lo equalled
# bias_pt_central on all 289 rows. The panel published an upside band and no
# downside band at all, which reads as "the estimate cannot be too high" --
# a claim nobody made and the data does not support.
#
# Deriving the tier here rather than patching the interim CSVs is deliberate:
# the pre-2013 extraction adds hundreds of rows written by other agents, and
# a rule enforced only by everyone remembering it is not enforced. An
# explicit TIER flag always wins (setdefault), and every derivation is
# REPORTED by validate_flags -- derived, never silent.
DERIVED_TIER = {
    "CASH_TAX_ALLOCATED_FROM_FY": ("cash_tax_paid", "C"),
    "GOLD_REV_ALLOCATED_FROM_FY": ("segment_revenue_gold", "C"),
}


def validate_flags(panel):
    """Check the flags the CODE reads. The others are documentation.

    EXTRACTION_CONTRACT.md calls its flag list a closed set. It is not one:
    56 distinct codes are in active use that the contract never defined, and
    most carry real information worth keeping (SUKARI_CONSOLIDATED_100PCT_...
    says something no generic code could). The workable split is not
    open-versus-closed but read-versus-descriptive.

    Exactly three flag families change a number:
      TIER<x>:<field>[:<code>]  -> the fidelity vector, and through it the grade
      CAT2_SUBSTITUTION         -> drops the row from the headline aggregate
      CAPINT_INCLUDED_IN_CAPEX  -> suppresses the capitalised-interest add-back
    Those are validated here. A TIER flag naming a field that does not exist,
    or a near-miss spelling of one of the three, currently fails SILENTLY: the
    regex simply does not match, the position falls through to its default
    tier, and the row grades as though the flag had never been written. That
    is the worst possible failure -- a correction that looks applied and isn't.
    """
    read_exact = {"CAT2_SUBSTITUTION", "CAPINT_INCLUDED_IN_CAPEX"}
    problems, descriptive = [], set()
    derived = {}
    for _, r in panel.iterrows():
        for raw in re.split(r"[;|]", str(r.get("flags") or "")):
            f = raw.strip()
            if not f:
                continue
            head = f.split(":")[0]
            if head.startswith("TIER"):
                m = TIER_RE.fullmatch(f) or TIER_RE.match(f)
                if not m:
                    problems.append(f"{r.ticker} {r.quarter}: unparseable tier flag {f!r}")
                elif m.group(2) not in FIDELITY_FIELDS:
                    problems.append(f"{r.ticker} {r.quarter}: tier flag names "
                                    f"unknown field {m.group(2)!r} in {f!r}")
            elif head in read_exact:
                pass
            else:
                descriptive.add(head)
                if head in DERIVED_TIER:
                    field, tier = DERIVED_TIER[head]
                    if f"TIER{tier}:{field}" not in str(r.get("flags") or ""):
                        derived.setdefault(f"{head} -> TIER{tier}:{field}",
                                           []).append(f"{r.ticker} {r.quarter}")
                # Near-miss on a machine-read code: same letters, different
                # punctuation or a dropped underscore. Silently inert today.
                squash = head.replace("_", "")
                for known in read_exact | {"TIER"}:
                    if squash == known.replace("_", "") and head != known:
                        problems.append(f"{r.ticker} {r.quarter}: {head!r} looks "
                                        f"like {known!r} but will not be read")
    for k, rows in sorted(derived.items()):
        problems.append(f"DERIVED (contract C.2: write both): {k} on {len(rows)} rows, "
                        f"e.g. {rows[0]}, {rows[-1]}")
    return problems, descriptive


def grade_fidelity(d):
    """Per-row fidelity vector, bias budget and composite grade (section 9)."""
    vectors, centrals, los, his, grades, headline, prefs, notes = [], [], [], [], [], [], [], []
    for _, r in d.iterrows():
        flags = str(r.get("flags") or "").replace("|", ";")
        explicit = {f: ("E" if t == "AEQ" else t)
                    for t, f, _ in TIER_RE.findall(flags)}
        # An explicit tier flag always wins; the derivation only fills a gap.
        for code, (field, tier) in DERIVED_TIER.items():
            if code in flags:
                explicit.setdefault(field, tier)
        price = r.get("realised_price")
        vec, central, lo, hi, unquant = [], 0.0, 0.0, 0.0, False

        for field in FIDELITY_FIELDS:
            if field in explicit:
                tier = explicit[field]
            elif field in d.columns and pd.notna(r.get(field)):
                # A real extracted value grades A even for a capping field --
                # that is the whole point of extracting it.
                tier = "A"
            elif field in UNQUANTIFIED_FIELDS:
                tier = "D"
            elif field not in d.columns or pd.isna(r.get(field)):
                # A null in a GROUP_COSTS column is not neutral: the build
                # fills it with zero, so the cost is silently omitted. Two
                # exceptions, both cases where the line was genuinely inside
                # another line rather than missing.
                pre_standard = int(str(r.quarter)[:4]) < STANDARD_ERA_AEQ.get(field, 0)
                tier = ("E" if pre_standard
                        or (r.ticker, field) in LEGACY_A_EQUIVALENT else "D")
            else:
                tier = "A"
            vec.append(tier)

            if tier in ("A", "E") or field not in BIAS_ANCHOR:
                if tier == "D" and field in UNQUANTIFIED_FIELDS:
                    unquant = True
                # A substitution on a field with no measured anchor is not a
                # zero-width band, it is an unmeasured one. segment_revenue_gold
                # is the case that bites: Agnico's 32 pro-rata revenue quarters
                # would otherwise report Tier C in the vector and +-0.00 beside
                # it, which reads as "substituted, and we know it cost nothing".
                # We do not know that. Marking it unquantified routes it through
                # section 11's capping rule instead of publishing a false zero.
                elif tier in ("B", "C", "D"):
                    unquant = True
                continue
            c, p90, outside = _anchor_at(field, price)
            unquant = unquant or outside
            if tier == "D":            # zeroed: the whole wedge is the error
                central += c; hi += p90
            elif tier == "B":          # substituted: half the wedge, centred
                central += c * 0.5; hi += p90 * 0.5
            # Tier C (pro-rata) is centred on zero by construction -- section 5
            # measures its error mean at ~0 -- so it moves only the band.
            if tier == "C":
                hi += c * 0.5; lo -= c * 0.5

        vector = "".join(vec)
        worst = max(TIER_ORDER[t] for f, t in zip(FIDELITY_FIELDS, vec)
                    if f not in UNQUANTIFIED_FIELDS)   # capping fields cap, they do not floor
        # Budget: half the trailing aggregate margin, capped at 2.5pt, floored
        # at 1.0 -- the same number section 11's H3 uses.
        base = r.get("L2") if pd.notna(r.get("L2")) else r.get("L1")
        budget = BUDGET_CAP if pd.isna(base) else min(BUDGET_CAP, max(BUDGET_FLOOR, 0.5 * base))

        if worst == 0:
            g = "A"
        elif worst == 1 and abs(central) <= 1.0 and not unquant:
            g = "B"
        elif worst <= 2 and abs(central) <= budget:
            g = "C"
        elif abs(central) <= budget and vec[0] in "AB" and vec[2] in "ABC" and vec[6] in "ABC":
            g = "D"
        else:
            g = "X"
        if unquant and g in ("A", "B"):
            g = "C"                                     # section 11 capping rule
        cat2 = "CAT2_SUBSTITUTION" in flags
        if cat2 and g in ("A", "B"):
            g = "C"

        vectors.append(vector); centrals.append(round(central, 2))
        los.append(round(central + lo, 2)); his.append(round(central + hi, 2))
        grades.append(g); headline.append(g != "X" and not cat2)
        prefs.append(None if pd.isna(price) else round(float(price), 0))
        notes.append("price outside the two measured anchors; magnitude unquantified"
                     if unquant and (pd.isna(price) or not
                        (ANCHOR_P_TROUGH <= float(price) <= ANCHOR_P_BULL)) else "")

    d = d.copy()
    d["fidelity_vector"] = vectors
    d["fidelity_grade"] = grades
    d["bias_pt_central"] = centrals
    d["bias_pt_lo"], d["bias_pt_hi"] = los, his
    d["bias_price_ref"] = prefs
    d["in_headline_aggregate"] = headline
    d["bias_note"] = notes
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
            # AISC-covered subset. The numerator can only sum periods that HAVE
            # an AISC, so the denominator must be the same periods. Dividing an
            # AISC covering one quarter by a full year of revenue printed
            # AngloGold 2018 as a 56.7% AISC margin when the covered period's
            # own figure is 12.5% -- a 44-point overstatement, on six annual
            # rows. Where coverage is partial the year is reported with an
            # explicit aisc_periods count rather than silently blended.
            cov = g[g.aisc_comparable.notna() & g.gold_oz_sold.notna()]
            aisc_usd = (cov.aisc_comparable * cov.gold_oz_sold).sum() / 1e6
            aisc_rev = (cov.realised_price * cov.gold_oz_sold).sum() / 1e6
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
                "aisc_margin": (None if not len(cov) or not aisc_rev
                                else round((1 - aisc_usd / aisc_rev) * 100, 2)),
                "aisc_periods": int(len(cov)), "aisc_all_periods": len(cov) == len(g),
                "aisc_weighted": (None if not len(cov)
                                  else round(aisc_usd * 1e6 / cov.gold_oz_sold.sum(), 0)),
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
    flag_problems, descriptive_flags = validate_flags(panel)
    frames = [grade_fidelity(add_smoothed(g)) for _, g in panel.groupby("ticker")]
    audit = censoring_audit(panel)

    cols = ["ticker", "quarter", "freq", "gold_revenue", "gold_oz_sold", "realised_price",
            "w_gold", "L0a", "L0b", "L0b_adj", "aisc_margin", "L1", "L2", "L2_n", "published_aisc",
            "aisc_comparable", "aisc_basis_note", "gold_cost_total", "total_revenue",
            "net_income_attributable", "impairment_charges",
            "aisc_ratio", "is_outlier", "L1_median_q", "L1_dev", "L1_scale_q",
            "panel_n_q", "L2_months", "months", "sector_distress", "sector_breach_share",
            "sector_breach_n", "sector_testable_n",
            "recon_residual_pct", "recon_residual_calc", "recon_basis_used",
            "fidelity_vector", "fidelity_grade", "bias_pt_central",
            "bias_pt_lo", "bias_pt_hi", "bias_price_ref",
            "in_headline_aggregate", "bias_note", "flags"]
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

    rr = out.recon_residual_calc.abs()
    gate = rr > 2.0
    print(f"\nAISC checksum (recomputed): {int(rr.notna().sum())} rows testable, "
          f"{int(gate.sum())} outside the contract's 2% gate")
    if gate.any():
        by_t = out[gate].groupby("ticker").agg(n=("quarter", "size"),
                                               worst=("recon_residual_calc",
                                                      lambda s: round(s.abs().max(), 1)))
        print(by_t.to_string())
    print(f"\nflag vocabulary: 3 machine-read families, "
          f"{len(descriptive_flags)} descriptive codes in use")
    if flag_problems:
        print("FLAG DEFECTS (these change a grade and fail silently):")
        for pr in flag_problems:
            print("  " + pr)
    print("fidelity grades: " + "  ".join(
        f"{g}={n}" for g, n in out.fidelity_grade.value_counts().sort_index().items()))
    print("bias_pt_central: mean %+.2f  max %+.2f  rows over budget: %d"
          % (out.bias_pt_central.mean(), out.bias_pt_central.max(),
             int((out.fidelity_grade == "X").sum())))
    worst = out.nlargest(5, "bias_pt_central")[
        ["ticker", "quarter", "fidelity_vector", "fidelity_grade", "bias_pt_central"]]
    print(worst.to_string(index=False))

    violations = out[out.aisc_margin <= out.L1]
    print(f"\ninvariant AISC margin > GAIM: {'HOLDS' if violations.empty else 'VIOLATED'}"
          f" ({len(violations)} exceptions)")
    if not violations.empty:
        print(violations[["ticker", "quarter", "aisc_margin", "L1"]].to_string(index=False))


if __name__ == "__main__":
    main()
