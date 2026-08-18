# Gold Mining Quarterly Margin — Methodology (口径定稿 v0.1 DRAFT)

> Status: DRAFT pending pilot validation. Not yet approved for production.
> Primary sources retrieved in full: WGC Guidance Note on Non-GAAP Metrics (June 2013
> original) and its November 2018 revision incl. 22 FAQs and 8 case studies.
> The 2018 note remains the operative standard — no 2023/2024/2025 revision exists.

## 0. Three published layers — the ladder

Every company-quarter is published at three levels. Each layer adds exactly one kind of
intervention, so the effect of every adjustment we make is visible by subtraction.

### L0 — As-reported profit (纯财报利润率). ZERO adjustment.
Lifted verbatim from the filing. Nothing added, nothing removed, nothing allocated,
nothing smoothed. This is the unarguable floor of the analysis.

```
L0a  Gold-segment operating margin
     = (segment revenue - segment cost of sales - segment DD&A) / segment revenue
       ... all three read directly off the IFRS 8 / ASC 280 segment note

L0b  Company net margin
     = net income attributable to owners / total revenue
       ... the most literal "profit in the financial report" there is; includes
           non-gold segments, published as-is without stripping them
```
L0 is the only layer that requires no judgement from us whatsoever, and therefore the
only one a reader can verify against the filing in under a minute. It is published for
every company-quarter where a financial statement exists — which, for a listed company,
is always. Where a company reports half-yearly, L0 is published half-yearly and labelled
as such; it is never interpolated.

### L1 — GAIM raw. Fully-loaded, forward-computed, NO outlier treatment.
The metric defined in §2. Every one-off — impairment quarters, strikes, tailings-dam
incidents, COVID stoppages, legal settlements — stays in. Lumpy by construction.

### L2 — GAIM trimmed. L1 plus the statistical trim in §11.
Two-sided 15% trim, median-biased. The smoothed reading.

**All three are charted together. The L0→L1 gap shows what full-cost loading does; the
L1→L2 gap shows what the trim removes. Neither gap is allowed to be invisible.**

## 1. Direction of the pipeline — READ THIS FIRST

**Financial statements are the INPUT. AISC/AIC is the CHECKSUM. Never the reverse.**

**The margin is computed FORWARD.** Gold-segment revenue is read directly off the segment
note / revenue-disaggregation note. It is NEVER reconstructed as (market gold price x ounces
sold). No external gold price series enters this pipeline at any point — introducing one
invites exactly the reverse-engineering this section exists to prevent. Where a company does
not state gold revenue as its own line (Newmont's earnings release), the figure is taken from
the 10-Q revenue-disaggregation note, which does split gold from copper and silver/lead/zinc.
If a filing genuinely lacks the split, the observation is flagged, not estimated from price.

```
Audited financial statements (income stmt, cash flow stmt, segment note)
        |
        |-- extract gold-segment line items
        |
        +---> compute GAIM  (our margin)
        |
        +---> reconstruct AISC per the WGC build-up
                     |
                     v
              compare against company-published AISC
                     |
        within tolerance -> our reading of the filing is CORRECT, GAIM is admissible
        outside tolerance -> we misread a line; reject and re-extract
```

Taking company-published AISC as a direct input would inherit every distortion baked into
it — by-product netting, management discretion over the sustaining/non-sustaining boundary,
the Nov-2018 reclassification — and would not be an analysis of the financials at all, merely
a re-expression of a non-GAAP number. The reconstruction step is what proves we understood
the filing.

**Tolerance gate: |reconstructed AISC - published AISC| / published AISC <= 2%.**
Observations outside the gate do not enter the series until the discrepancy is explained.
The residual itself is stored — a persistent one-directional residual for a given company
signals a systematic misreading, not noise.

## 2. Headline metric — the 口径

**GAIM — Gold All-In Margin**, expressed as a percentage of gold revenue. Every term is a
line item lifted from the financial statements, not a company-computed metric:

```
          R_Au  - OpCost_Au        (cost of sales EXCLUDING DD&A, gold segment)
                - Royalties_Au     (royalties & production taxes)
                - CorpG&A_Au       (allocated, see §7)
                - Explor_Au        (EXPENSED exploration ONLY - capitalised
                                    exploration already sits inside Capex_Au)
                - Capex_Au         (TOTAL capex from the cash flow statement,
                                    sustaining AND growth - no split required)
                - Reclam_Au        (accretion + ARC amortisation - ONLY where not already
                                    bundled inside finance costs; see non-overlap rule)
                - Lease_Au         (lease principal + financing component)
                - NetInt_Au        (interest expense - interest income, incl. capitalised)
                - CashTax_Au       (cash taxes PAID, not the P&L charge)
                - OneOff_Au        (M&A fees, litigation settlements, severance)
GAIM =    ---------------------------------------------------------------------
                                        R_Au
```

**DD&A is excluded from the cost stack and total capex is used instead.** Using both would
double-count the same capital. This is a cash-economics measure, consistent with the AIC
logic, and it is why no sustaining/growth capex split is needed — which is precisely what
makes the pre-2013 backcast tractable (§8).

Construction rules, all non-negotiable:

| Rule | Choice | Why |
|---|---|---|
| Reconciliation anchor | **AIC**, not AISC | AIC is invariant to the Nov-2018 WGC reclassification (Gold Fields: AISC 973→891, AIC unchanged at 1,106). The largest definitional break in 2005–2026 does not touch it — so AIC is the stabler *reconciliation target*. AISC is reconstructed too, as the second checksum. |
| Units | **% of gold revenue**, not $/oz spread | Co-product-neutral, cannot go negative from by-product credits, commodity-agnostic, directly comparable across different metal mixes. |
| Numerator | **Realised** gold revenue R_Au, never spot × ounces | Only way hedge losses (critical 2005–2010) and streaming leakage enter the metric at all. |
| Basis | **Attributable**, never consolidated | Cash at a 61.5%-owned mine is not 100% available to parent shareholders. |
| Denominator | **Ounces sold**, restated where a company reports per ounce *produced* | WGC specifies sold; Agnico reports produced. Production≠sales creates several % of pure measurement noise. |
| By-product | **Co-product restated** on relative revenue | See §5. |
| Frequency | Quarterly observations, **trailing-4-quarter headline** | De-lumps growth capex without destroying quarterly frequency. |

## 3. What GAIM adds relative to AISC

AISC answers: *does a mine cover the cost of staying open?*
GAIM answers: *does the business cover the cost of existing?*

| # | Item absent from AISC | Shareholder-borne? | In GAIM |
|---|---|---|---|
| 1 | Non-sustaining / growth / expansionary capex | YES, in full — cash out the door | **ADD** (largest single omission; primary gaming vector) |
| 2 | Non-sustaining / greenfield exploration & study | YES — reserve replacement is COGS in disguise | **ADD** |
| 3 | Income taxes | YES — first claim on gross margin | **ADD** as *cash taxes paid*, not P&L charge |
| 4 | Interest / finance costs, incl. capitalised interest | YES | **ADD** net (interest expense − interest income) |
| 5 | M&A costs — advisory, break, integration fees | YES — excluded from AIC too, not just AISC | **ADD** |
| 6 | Litigation costs & settlements | YES — newly excluded by the 2018 revision | **ADD** |
| 7 | One-time material severance | YES — "one-time" repeated across cycles is an operating cost | **ADD** |
| 8 | Minority-interest leakage | YES — basis choice, not a cost | **DEDUCT** via attributable basis |
| 9 | Purchase price of acquired ounces | YES — a miner that buys rather than finds shows clean AISC | **FLAG** (structurally invisible; disclosed as a diagnostic, not capitalised into the margin) |
| 10 | Streamed / royalty-encumbered ounces | YES — real value transfer | Captured automatically by using realised revenue |
| 11 | Working capital movements | YES but timing-only; mean-reverting | **EXCLUDE** from headline (imports a seasonal sawtooth); carried in the FCF cross-check |
| 12 | Impairments & write-downs | AMBIGUOUS | **DO NOT ADD — would double-count item 1.** Tracked as a validation diagnostic: persistent impairments prove the growth-capex charge was justified. |
| 13 | Stock-based compensation | YES | **ALREADY IN AISC** (lines h, m; FAQ 20). Do not add back. Watch for companies reporting an "adjusted" AISC that strips it. |

**The gap between the AISC margin and GAIM is the product.** It is the quantified answer to
"what does AISC hide?" — report it on every chart.

## 4a. The reconstruction (checksum) formula

Built from the SAME extracted line items that feed GAIM, following the WGC 2018 build-up:

```
reconstructed AISC/oz = [ OpCost_Au + Royalties_Au + CorpG&A_Au
                        + SustainingExplor_Au + SustainingCapex_Au
                        + Reclam_Au + SustainingLease_Au
                        - ByProductCredits ] / oz sold
```

Note this reconstruction DOES require the sustaining/growth split — but only as a *validation*
step against a published figure, never as an input to GAIM. If a company does not disclose the
split, the reconciliation falls back to AIC (which needs no split) and the AISC checksum is
skipped, with the observation flagged `NO_AISC_CHECK`.

Denominator: **ounces sold**. Restate where a company reports per ounce *produced* (Agnico).

## 4b. Cross-checks carried alongside (never dropped)

- **AISC margin** `(P̄ − AISC)/P̄` — market/sell-side consensus reference. The GAIM-vs-AISC gap is the headline diagnostic.
- **GAAP segment EBIT margin** — the only series with genuine quarterly coverage back to 2005 (IAS 14 pre-2009, IFRS 8 / ASC 280 after), and the only one available for non-WGC filers such as Zijin. Independently auditable. Used to validate the pre-2013 backcast: if reconstructed GAIM and observed segment EBIT margin co-move in 2013–2019 where both exist, the backcast is credible.
- **FCF margin** — annual only, plus a cumulative 2005–2026 reconciliation. Terminal honesty check on the allocation assumptions.

## 5. By-product problem and the co-product restatement

Under by-product accounting `∂AISC/∂P_Cu = −Q_Cu/Q_Au` — strictly negative and independent of
any mining variable. Reported gold cost falls when copper rallies; it can go negative
(Snowden Optiro worked example: −$250/oz while incurring substantial real costs).

Measured magnitude: **Newmont FY2025 by-product AISC $1,358/oz vs co-product $1,609/oz — a
$251/oz, ~18% wedge from presentation choice alone.**

Because gold and copper are positively correlated at multi-year horizons, this contamination is
*systematically* correlated with our numerator — any regression of margin on gold price using
by-product AISC is biased. Restatement procedure:

1. Recover credits from the AISC reconciliation table (disclosure required by Note 1 / FAQ 1).
2. Gross up: `AISC_gross = AISC_reported + credits/oz`.
3. Recover revenue by metal from the IFRS 15 / ASC 606 disaggregation note (reliable from 2018).
4. `w_Au = Rev_Au / (Rev_Au + Rev_other)`.
5. `AISC_coproduct = w_Au × AISC_gross_total / Au oz sold`.

Expressing GAIM as % of revenue means the allocation only ever *bounds* rather than eliminates
price sensitivity — state it as an assumption, not a fact.

### Presentation basis by company (verified)
| Company | Basis | Note |
|---|---|---|
| Newmont | Co-product | CAS allocated on relative sales value |
| Agnico Eagle | Both, reconciled | Reports per ounce **produced** — restate to sold |
| Barrick | By-product headline | "Co-product" appears gross-of-credits, NOT a true reallocation — verify before use |
| Kinross | By-product | Silver netted |
| Gold Fields | **Gold-equivalent ounces** at Cerro Corona | A third convention; GEO embeds a price ratio that drifts |
| Freeport | By-product + full co-product | Copper primary |
| Zijin | Neither — unit cost by product line | No AISC at all |

## 6. Coverage tiers — publish alongside every observation

- **Tier 1 — pure gold** (Agnico, AngloGold, Gold Fields, Kinross, Barrick gold segments): full metric.
- **Tier 2 — gold-primary polymetallic** (Newmont, Barrick group, Zijin): metric with co-product restatement, by-product/co-product spread reported as an uncertainty band.
- **Tier 3 — gold as by-product** (Freeport): **excluded from the margin series**, volume-only. There is no gold-only cost function at Grasberg — same ore, same mill, same trucks. Any gold-only margin is an artefact of the allocation rule.

A margin series that silently mixes tiers is not comparable.

## 7. Corporate overhead allocation

Base case: **pro-rata on segment revenue** — `G&A_Au = G&A_corp × (Rev_Au/Rev_total)`. Internally
coherent with the co-product logic in §5.
Sensitivities reported: pro-rata on segment operating cost / capital employed; pro-rata on production volume.
Where a company is ~pure gold, prefer the disclosed **company-level** AIC, which already includes
corporate G&A by construction (2018 Note 6) — the allocation question dissolves.
**If the spread across conventions exceeds ~1.5 margin points, flag the observation as allocation-sensitive.**

Net interest: allocate on segment capital employed where segment assets are disclosed; fall back to revenue.
Cash tax: allocate on gold revenue; prefer jurisdictional allocation where country-by-country reporting exists (2024+).

## 8. Pre-2013 backcast (2005–2012)

AISC did not exist before June 2013. No rigorous published backcast exists — we own this
methodology risk entirely.

Predecessor standards (distinct lineages, commonly conflated):
- **Gold Institute Production Cost Standard (1996)** — the gold-industry ancestor of AISC.
  Cash Operating Costs → Total Cash Costs (+royalties, production taxes, net of by-product credits)
  → Total Production Costs (+D&A, reclamation).
- **Brook Hunt / Wood Mackenzie C1/C2/C3** — a *base-metals* taxonomy applied to gold by analysts.
  C1 ≈ Gold Institute Total Cash Cost ≈ WGC sub-total (l). C3 uniquely includes net interest.

Neither C2 nor C3 contains sustaining capex — they carry D&A instead. **D&A is a historical-cost
proxy for sustaining capital, not a substitute**; in a period of rising unit capital intensity
(2005–2012 was exactly that) it materially understates it.

```
pseudo-AIC_t = TotalCashCost_t                       [disclosed — HIGH confidence]
             + CorporateG&A_t / Q_t                  [income statement — HIGH]
             + ReclamationAccretion_t / Q_t          [ARO note — MEDIUM]
             + TotalCapex_t / Q_t                    [cash flow — HIGH]
             + TotalExploration_t / Q_t              [HIGH]
```

**pseudo-AIC needs only *total* capex — no sustaining/growth split at all.** This is the second
decisive argument for the AIC anchor: the backcast error band is roughly half that of pseudo-AISC
(±4–6% vs ±8–12% per company-quarter).

Validation exhibit — **Barrick FY2012**, which built this metric before WGC finalised the standard:

| Component | US$/oz | % of uplift |
|---|---|---|
| Total cash costs | 584 | — |
| Minesite sustaining capital | 155 | 42.9% |
| Mine development | 114 | 31.6% |
| Corporate admin (gold) | 51 | 14.1% |
| Exploration/evaluation | 21 | 5.8% |
| Environmental rehabilitation | 20 | 5.5% |
| **All-in sustaining costs** | **945** | |

Uplift = $361/oz — **AISC was 61.8% above total cash cost in 2012.** This ratio is our prior.

### Known biases — all one-directional, all making pre-2013 pseudo-AISC too LOW
1. **IFRIC 20** (1 Jan 2013): IFRS filers began capitalising production-phase stripping — breaks the cash-cost sub-total across 2013.
2. **No sustaining/non-sustaining classification existed pre-2013**, so no incentive to reclassify capex downward. Pre-2013 pseudo-AISC is built on a *stricter* basis than post-2019 reported AISC. Combined with the 2018 revision's −8.4%, a naive 2005→2026 AISC series shows a **spurious downward cost trend of ~8–12% concentrated at 2019**. Correct explicitly or use AIC.
3. **Leases**: continuous only if WGC lines (s)/(cc) are populated. Verify per company — the patch is voluntary.
4. **Hedge books**: 2005–2010 realised ≠ spot for Barrick, AngloGold and others. Use realised revenue always.
5. **IFRS transition 2005**: EU/AU/ZA filers moved to IFRS at the very start of the window — Gold Fields, AngloGold, Harmony, Newcrest segment data is not comparable across that line.

## 9. Mandatory break flags on every observation

`IFRS_ADOPT_2005` · `IFRIC20_2013` · `WGC_REV_2019` · `IFRS16_ASC842_2019` · `ASU2023-07_FY2024`
plus entity-level: `AU_REDOMICILE_2023` (AngloGold CIK 1067428→1973832), `BARRICK_TICKER_2025` (GOLD→B),
`CDN_GAAP_IFRS_2011` (Barrick/Agnico/Kinross).

## 10. Structural non-comparabilities that cannot be fixed, only disclosed

- **US GAAP filers cannot capitalise production-phase stripping** (EITF 04-6); **IFRS filers can** (IFRIC 20). WGC FAQ 10 concedes this openly. Newmont is structurally non-comparable to Barrick/AngloGold/Gold Fields on this line, permanently.
- **IFRS 8 does not prescribe a segment-profit measure** — it mandates disclosure of whatever measure management uses. Two miners can disclose "segment profit" meaning different things; one miner can change it. Read the accounting policy note every year.
- **Reclamation accretion is a discount-unwind** — a function of the discount rate, not of mining. Falling rates 2005–2021 suppressed it; rising rates 2022+ inflated it. Consider substituting a straight-line LOM-amortised closure provision at a fixed real rate.


## 11. Outlier treatment and smoothing (L2)

**One exclusion rule, and it is economic rather than statistical.**

```
A company-quarter is dropped from the aggregate when
    published AISC / realised gold price  >  0.80
i.e. when all-in sustaining cost consumes more than 80% of revenue.
Survivors are aggregated revenue-weighted, then smoothed with a
trailing 4-quarter average.
```

The purpose is narrow and specific: stop one company's distressed year dragging the
industry average down. A miner running at a 90% cost ratio is not telling you about
the sector, it is telling you about itself.

**Why a flat threshold rather than a statistical trim.** An earlier version trimmed
the extreme values inside a rolling window. That method cannot distinguish a
company-specific one-off from a genuine sector-wide move, and in practice it deleted
the latter — it discarded Barrick's real 2022 cost-shock trough from seven
consecutive windows and lagged every turning point, because in a trending series the
newest observation is almost always the window extreme. A fixed economic threshold
has neither failure mode: the 2022 cost inflation hit all four companies at once, so
it stays in as trend, exactly as it should.

**Aggregate first, then smooth.** Because an industry-wide event appears in every
company simultaneously, after aggregation it *is* the curve's own trend and survives.
Only company-specific one-offs get diluted. This ordering is deliberate.

**Revenue-weighted, never a mean of ratios.** Sum gold revenue and total cost across
the selected companies and divide once. Averaging four margins would weight a $4bn
company the same as a $1bn one and produce a number corresponding to no real entity.

**Current bite: zero.** No observation in the 88-quarter pilot reaches the threshold;
the worst is Newmont 2023Q2 at 77.9%. The rule is a guard for extending the series
back through the 2013-2015 trough and for admitting high-cost South African miners.
Every exclusion it ever makes is logged to `data/final/trimmed_observations.csv` with
the AISC, the realised price and the ratio, so it can be checked by hand.

**Timing artefacts are fixed at source, not smoothed over.** Agnico's Q1 2026 cash
tax included $1.3bn the company itself attributes to the 2025 tax year; it is
reallocated to 2025 pro-rata on gold revenue and flagged, rather than left as a
44%-of-revenue lump for the smoother to hide.

## 12. Open items before production
1. Confirm Barrick's "co-product" definition in the FY2024 40-F — suspected gross-of-credits.
2. Verify hedge-book history (Barrick Q3 2009 close, AngloGold 2010) and quantify realised-vs-spot gaps 2005–2010.
3. Montana Tech theses on AISC construction — HTTP 403, need institutional access.
4. S&P Global Market Intelligence — how far back does their gold AISC series run, and is any of it backcast?


## 13. Two non-negotiable arithmetic rules (found in Round 1, not theory)

**Rule 1 — the cost stack must be EXHAUSTIVE AND NON-OVERLAPPING.**
Round 1 caught two real double-counts in the formula as first drafted:
- `exploration_total` + `capex_total`: capitalised exploration sits inside capex. Agnico 2026Q2
  proves it — sustaining capex 236,950 + sustaining cap.expl. 8,843 + development capex 462,274 +
  development cap.expl. 92,853 + WC adj 8,335 = additions to PP&MD 809,255. Subtracting an
  all-in exploration figure as well double-charges $101,696k = **2.7 points of gold revenue**.
  → `exploration_total` is the EXPENSED line only.
- `net_interest` + `reclamation_accretion`: Agnico's `Finance costs` is a gross bundle already
  containing reclamation accretion and lease interest. Subtracting accretion again double-charges it.
  → where a component is bundled into another captured line, it is NOT taken separately. Record null,
  not zero.

**Rule 2 — the checksum is a checksum, not an anchor.**
Reconstruct whichever all-in figure the company actually published for that period and tie to it.
**If AIC is not published, use AISC. If neither, skip the check and flag it.** The purpose is only
to prove we read the filing correctly. Barrick stopped publishing AIC after 2024Q2 and co-product
after 2025Q3 — that is not a methodology problem, it just means AISC is the tie-out for those
quarters. Never self-compute a figure and then "verify" against it.
