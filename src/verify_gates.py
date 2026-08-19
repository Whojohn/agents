#!/usr/bin/env python3
"""The verification gates that replace the AISC checksum before 2013Q3.

AISC did not exist until the WGC guidance note of June 2013, so the reconciliation
that anchors the 2013-2026 panel simply has nothing to run against in 2005-2012.
DEGRADATION section 7.4 specifies the replacement set. This module implements it.

Four gates, and the honest state of each:

  1. IMPLIED PRICE CONVERGENCE  -- computable today.
     Cross-company dispersion of gold revenue / ounces sold inside a period.
     It validates the DENOMINATOR only. It says nothing about whether any line
     in the cost stack was read correctly, and section 7.4 explicitly retracts
     the v1 claim that its 1.4% convergence was "tight enough to replace the
     AISC check". Passing this gate is not evidence the costs are right.

  2. ANNUAL RECONCILIATION      -- NOT computable: extraction does not store the
     audited annual figure alongside the quarters, so there is nothing to sum
     against. Needed columns named in GATE2_NEEDS. Two documented holes even
     once it runs: zero power against fields that were pro-rated FROM the annual
     figure, and zero power against annual-frequency observations.

  3. DUAL-SOURCE CONSISTENCY    -- NOT computable: needs capex against the PP&E
     additions roll-forward and cash tax against the tax note's own "taxes paid"
     line. Neither is extracted. Columns named in GATE4_NEEDS.

  4. PSEUDO-AIC COST RATIO      -- computable today. The exclusion rule that
     works without a published AISC (section 7.5).

Gates 2 and 3 are the ones that would constrain capex, cash tax and net
interest -- roughly 38% of the GAIM cost stack. Until the extraction supplies
their columns, that 38% carries NO verification in the pre-2013 era beyond the
crude [0.20, 1.20] range check. This module reports that as a blocked gate
rather than quietly scoring three gates out of four.
"""
import pathlib
import sys

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

ROOT = pathlib.Path(__file__).resolve().parent.parent
INTERIM, FINAL = ROOT / "data/interim", ROOT / "data/final"

PRICE_TOL_PCT = 3.0      # section 7.4 gate 1
ANNUAL_TOL_PCT = 0.5     # section 7.4 gate 3 -- rounding only
DUAL_TOL_PCT = 3.0       # section 7.4 gate 4
PAIC_RATIO_CAP = 0.80    # section 7.5, mirrors AISC_RATIO_CAP

GATE2_NEEDS = ["fy_audited_gold_revenue", "fy_audited_opcost_ex_dda",
               "fy_audited_capex_total", "fy_audited_cash_tax_paid"]
GATE4_NEEDS = ["capex_ppe_additions", "cash_tax_paid_alt"]

PAIC_SITE = ["opcost_ex_dda", "royalties"]
PAIC_GROUP = ["corporate_g_and_a", "exploration_expensed", "capex_total",
              "reclamation_accretion"]


def _half(period):
    """Half-year label, or None for an annual row.

    Fourth place this pipeline died on int('Y'). '2005FY' is Kinross's only
    2005 observation -- it filed nothing interim that year -- and a 12-month
    figure has no half to belong to. Returning None says so; returning
    '2005H1' would be a claim the filing never made.
    """
    kind = period[4]
    if kind in "FA":
        return None
    year, n = int(period[:4]), int(period[5:])
    return f"{year}H{n if kind == 'H' else (1 if n <= 2 else 2)}"


def gate_price_convergence(panel):
    """Gate 1. Implied realised price vs its same-period peers.

    Peers are rows carrying the SAME period label, not the same half-year. A
    quarterly row measured against a six-month reference picks up the intra-half
    price move instead of an extraction error: in 2025H2 gold ran from about
    $3,460 to $4,180, which threw four of five quarterly rows outside a 3% band
    while nothing was wrong with any of them. Section 7.4's measured 1.4%
    dispersion was a WITHIN-QUARTER cross-company figure, so the gate has to be
    one too.

    A row whose period label has fewer than MIN_PEERS companies is reported
    untestable rather than scored. Half-yearly filers mostly land here, which is
    the honest answer: with two half-yearly filers in the panel there is no
    convergence to measure, only a two-point spread.
    """
    MIN_PEERS = 3
    d = panel.copy()
    # Use the panel's own realised_price. Do NOT recompute it as
    # gold_revenue / gold_oz_sold: for Barrick those two columns are on
    # DIFFERENT bases -- revenue is consolidated so it matches the consolidated
    # cost stack, ounces are attributable -- and dividing them yields $5,576/oz
    # for 2025Q4 against a market price near $4,000. The build already pairs
    # attributable revenue with attributable ounces for the price.
    d["implied_price"] = d.realised_price
    d["half"] = d.quarter.map(_half)
    # Numerator and denominator must cover the SAME rows. price * oz is NaN
    # wherever the price is missing and pandas drops it from the sum, but the
    # ounces were still counted in tot_oz -- so every company that discloses
    # ounces without a gold revenue line inflated the denominator alone and
    # halved the benchmark. Kinross does exactly that for 18 quarters
    # (2006Q3-2010Q3: metal sales are one line, the gold/silver split starts in
    # 2011), and the gate answered by declaring Newmont's 2007Q4 price 111% above
    # its peers. It was 0.6% above the London average. Restricting both sums to
    # rows carrying both figures is the whole fix; it is the same
    # numerator-population defect the annual AISC rollup already carries a
    # comment about, in a second function.
    d["_ok"] = d.realised_price.notna() & d.gold_oz_sold.notna()
    d["_rev"] = (d.realised_price * d.gold_oz_sold).where(d._ok)
    d["_oz"] = d.gold_oz_sold.where(d._ok)
    grp = d.groupby("quarter")
    d["peer_n"] = grp._ok.transform("sum")
    # Leave-one-out reference, so a single bad row cannot drag the benchmark
    # toward itself and hide inside it.
    d = (d.join(grp._rev.sum().rename("tr"), on="quarter")
          .join(grp._oz.sum().rename("to"), on="quarter"))
    d["panel_price"] = ((d.tr - d._rev.fillna(0))
                        / (d.to - d._oz.fillna(0)))
    d["price_dev_pct"] = (d.implied_price - d.panel_price) / d.panel_price * 100
    # peer_n counts rows WITH a price; the row itself is left out of the
    # benchmark, so it must be left out of the count that decides testability.
    d["peer_n"] = d.peer_n - d._ok.astype(int)
    d["gate1_testable"] = (d.peer_n >= MIN_PEERS) & d.panel_price.notna() \
                          & d.implied_price.notna()
    d["gate1_pass"] = ~d.gate1_testable | (d.price_dev_pct.abs() <= PRICE_TOL_PCT)
    return d[["ticker", "quarter", "half", "peer_n", "implied_price", "panel_price",
              "price_dev_pct", "gate1_testable", "gate1_pass"]]



# Quarterly average London gold price, USD/oz, rounded to the dollar. This is a
# REFERENCE for a diagnostic, never an input: no published figure in this
# project is computed from it, and the extraction contract's ban on external
# sources is about figures that enter the dataset. It earns its place because
# gate 1 is a leave-one-out PEER test, and a peer test can only say that one
# company differs from the others -- it cannot say which of them is wrong. With
# four constituents before 2011 that is a real weakness. An absolute reference
# resolves it, and did: it showed AngloGold 8-31% below market for 24
# consecutive quarters ending exactly at 2010Q4, which is its hedge book (closed
# 2010-10-07), and it showed Agnico ABOVE market in the quarters where its gold
# revenue is a residual after by-product credits -- contamination, not a price.
LONDON_GOLD_Q = {
    "2005Q1": 427, "2005Q2": 427, "2005Q3": 440, "2005Q4": 485,
    "2006Q1": 554, "2006Q2": 628, "2006Q3": 622, "2006Q4": 614,
    "2007Q1": 650, "2007Q2": 667, "2007Q3": 681, "2007Q4": 787,
    "2008Q1": 925, "2008Q2": 896, "2008Q3": 871, "2008Q4": 795,
    "2009Q1": 909, "2009Q2": 922, "2009Q3": 960, "2009Q4": 1100,
    "2010Q1": 1109, "2010Q2": 1197, "2010Q3": 1227, "2010Q4": 1367,
    "2011Q1": 1386, "2011Q2": 1509, "2011Q3": 1702, "2011Q4": 1688,
    "2012Q1": 1691, "2012Q2": 1611, "2012Q3": 1652, "2012Q4": 1721,
}
REF_TOL_PCT = 8.0   # wide: realised price legitimately differs from the average
                    # by timing of sales within the quarter and by provisional
                    # pricing. 8% is well outside that and inside the hedge
                    # discount, which ran to 31%.


def gate_reference_price(panel):
    """Gate 5. Realised price against the market average for the same quarter.

    Only quarters are testable: a half-year or annual row spans a window the
    quarterly reference cannot represent without averaging, and averaging is the
    step that hides the thing this gate looks for.
    """
    d = panel.copy()
    d["ref_price"] = d.quarter.map(LONDON_GOLD_Q)
    d["ref_dev_pct"] = (d.realised_price - d.ref_price) / d.ref_price * 100
    d["gate5_testable"] = d.ref_price.notna() & d.realised_price.notna()
    d["gate5_pass"] = ~d.gate5_testable | (d.ref_dev_pct.abs() <= REF_TOL_PCT)
    return d[["ticker", "quarter", "realised_price", "ref_price", "ref_dev_pct",
              "gate5_testable", "gate5_pass", "is_outlier",
              "in_headline_aggregate"]]

def gate_paic_ratio(interim, panel):
    """Gate 4 / section 7.5. Forward-computed cost ratio, no published AISC.

    Group costs are scaled by w_gold because they are company-level, not
    gold-segment; site costs are already gold-segment. A row missing any
    component is reported as untestable rather than scored with a zero in the
    numerator -- a zeroed component makes the ratio look BETTER, so scoring it
    would let the worst-documented rows pass most easily.
    """
    w = panel.set_index(["ticker", "quarter"]).w_gold
    d = interim.copy().set_index(["ticker", "quarter"])
    # Denominator must be the basis the COST stack is on. Barrick reports gold
    # revenue twice -- attributable (which backs the price) and consolidated
    # (which backs the costs) -- and dividing consolidated costs by attributable
    # revenue prints a cost ratio above 1.00 for a profitable quarter. The map
    # is imported rather than restated so it cannot drift from the build.
    from build_series import REVENUE_BASIS, DEFAULT_BASIS
    tickers = d.index.get_level_values("ticker")
    rev = pd.Series(float("nan"), index=d.index, dtype="float64")
    for t in tickers.unique():
        col = REVENUE_BASIS.get(t, DEFAULT_BASIS)[0]
        col = col if col in d.columns else DEFAULT_BASIS[0]
        rev.loc[tickers == t] = d.loc[tickers == t, col].astype("float64")
    have = [c for c in PAIC_SITE + PAIC_GROUP if c in d.columns]
    missing = [c for c in PAIC_SITE + PAIC_GROUP if c not in d.columns]
    site = sum(d[c].fillna(0) for c in PAIC_SITE if c in d.columns)
    group = sum(d[c].fillna(0) for c in PAIC_GROUP if c in d.columns)
    # A null is only a hole when the line is genuinely missing. Where the row
    # carries TIERAEQ:<field>:... the cost sits inside another line that IS in
    # the numerator, so treating the null as incomplete would mark the
    # best-documented rows untestable and leave the gate running on 52 of 289.
    flg = d["flags"].astype(str).str.replace("|", ";", regex=False)
    ok = []
    for c in have:
        bundled = flg.str.contains(f"TIERAEQ:{c}:", na=False)
        ok.append(d[c].notna() | bundled)
    complete = pd.concat(ok, axis=1).all(axis=1)
    ratio = (site + group * w.reindex(d.index)) / rev
    out = pd.DataFrame({"paic_ratio": ratio, "paic_complete": complete}).reset_index()
    out["gate4_testable"] = out.paic_complete & out.paic_ratio.notna()
    out["gate4_pass"] = ~out.gate4_testable | (out.paic_ratio <= PAIC_RATIO_CAP)
    out.attrs["missing_columns"] = missing
    return out


def blocked_gates(interim):
    """Gates 2 and 3: report exactly which columns are absent, per company.

    Reported as BLOCKED, never as passed. A gate that cannot run is not a gate
    that was satisfied, and the pre-2013 extraction has to be told which columns
    to capture for it to ever run.
    """
    rows = []
    for name, needs in [("annual reconciliation", GATE2_NEEDS),
                        ("dual-source capex/tax", GATE4_NEEDS)]:
        for col in needs:
            present = sorted(interim.loc[interim[col].notna(), "ticker"].unique()) \
                if col in interim.columns else []
            rows.append({"gate": name, "column": col,
                         "present_for": ";".join(present) or "(none)",
                         "n_rows": int(interim[col].notna().sum())
                                   if col in interim.columns else 0})
    return pd.DataFrame(rows)


def clear_circular_tcc(interim):
    """Section 7.3's most important sentence, enforced.

    If opcost_ex_dda was itself reconstructed from the published Total Cash Cost
    (TIERB:opcost_ex_dda:GI_TCC_GROSSED), then checking our opcost against that
    same TCC compares the number with itself. TCC_ONLY_CHECK must be cleared
    from such a row -- leaving it writes a "passed" line into the verification
    log that verifies nothing, which is worse than no check at all.
    """
    f = interim["flags"].astype(str).str.replace("|", ";", regex=False)
    circular = (f.str.contains("GI_TCC_GROSSED", na=False)
                & f.str.contains("TCC_ONLY_CHECK", na=False))
    return interim.index[circular].tolist()


def load_interim():
    files = (sorted(INTERIM.glob("*_quarterly.csv")) + sorted(INTERIM.glob("*_halfyearly.csv"))
             + sorted(INTERIM.glob("*_mixed.csv")))
    if not files:
        raise SystemExit("no extracted company files in data/interim/")
    return pd.concat((pd.read_csv(p) for p in files), ignore_index=True)


def main():
    panel = pd.read_csv(FINAL / "margins.csv")
    interim = load_interim()
    if "ticker" in interim:
        interim["ticker"] = interim.ticker.astype(str).str.split("/").str[0]

    g1 = gate_price_convergence(panel)
    n1 = int(g1.gate1_testable.sum())
    f1 = g1[g1.gate1_testable & ~g1.gate1_pass]
    print(f"gate 1  implied price convergence (<= {PRICE_TOL_PCT}%): "
          f"{n1} of {len(g1)} testable, {len(f1)} outside")
    if len(f1):
        print(f1.reindex(f1.price_dev_pct.abs().sort_values(ascending=False).index)
                [["ticker", "quarter", "implied_price", "panel_price", "price_dev_pct"]]
                .head(12).to_string(index=False))
    print("        NOTE: this gate validates the DENOMINATOR only. It is not "
          "evidence that any cost line was read correctly (section 7.4).")

    g5 = gate_reference_price(panel)
    n5 = int(g5.gate5_testable.sum())
    f5 = g5[g5.gate5_testable & ~g5.gate5_pass]
    inagg = f5[~f5.is_outlier & f5.in_headline_aggregate]
    print(f"\ngate 5  realised price vs London market (<= {REF_TOL_PCT}%): "
          f"{n5} of {len(g5)} testable, {len(f5)} outside, "
          f"{len(inagg)} of those inside the headline aggregate")
    if len(f5):
        print(f5.reindex(f5.ref_dev_pct.abs().sort_values(ascending=False).index)
                [["ticker", "quarter", "realised_price", "ref_price",
                  "ref_dev_pct", "in_headline_aggregate"]]
                .head(12).to_string(index=False))
    print("        Failing is not the same as wrong. AngloGold's run of negative "
          "deviations to 2010Q3 is its hedge book and belongs in the series; "
          "Agnico's positive ones are by-product contamination and are already "
          "trimmed. Read this gate as 'explain each of these', not 'drop them'.")

    g4 = gate_paic_ratio(interim, panel)
    n4 = int(g4.gate4_testable.sum())
    f4 = g4[g4.gate4_testable & ~g4.gate4_pass]
    print(f"\ngate 4  pseudo-AIC cost ratio (<= {PAIC_RATIO_CAP:.2f}): "
          f"{n4} of {len(g4)} testable, {len(f4)} over cap")
    if g4.attrs["missing_columns"]:
        print(f"        columns absent from the panel: {g4.attrs['missing_columns']}")
    if len(f4):
        print(f4.nlargest(10, "paic_ratio")[["ticker", "quarter", "paic_ratio"]]
                .to_string(index=False))
    over_2013 = f4[f4.quarter.str[:4].astype(int) <= 2016]
    print(f"        DIAGNOSTIC ONLY, it excludes nothing. {len(over_2013)} of "
          f"{len(f4)} breaches fall in 2016 or earlier, when cost ratios near 1.00 were "
          f"the industry's actual condition rather than an extraction fault -- "
          f"using this as an exclusion rule would delete the trough it is "
          f"supposed to measure (the same defect the AISC ratio cap has).")

    print("\nblocked gates -- these cannot run, and are NOT counted as passed:")
    print(blocked_gates(interim).to_string(index=False))

    circ = clear_circular_tcc(interim)
    print(f"\ncircular TCC checks to clear (section 7.3): {len(circ)}")

    FINAL.mkdir(parents=True, exist_ok=True)
    g1.to_csv(FINAL / "gate_price_convergence.csv", index=False)
    g4.to_csv(FINAL / "gate_paic_ratio.csv", index=False)
    g5.to_csv(FINAL / "gate_reference_price.csv", index=False)
    blocked_gates(interim).to_csv(FINAL / "gates_blocked.csv", index=False)
    print(f"\nwrote 4 gate logs to {FINAL}")
    print("\n2013 前的净结论：capex + 现金税 + 净利息（约占 GAIM 成本栈 38%）"
          "在闸门 2 与 3 落地之前没有任何独立验证。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
