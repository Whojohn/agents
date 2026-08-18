# Round 1 Discovery — Newmont (NEM), CIK 0001164727

Periods worked in full: **2026Q1** and **2021Q2**. All figures USD millions unless stated.
Parsed from local files with BeautifulSoup/lxml. No WebFetch. No margin computed.

## Resolved: gold revenue IS a stated line item

The earlier reconnaissance claim that Newmont does not state gold revenue, and that it must be
derived as (realised price x ounces), is **wrong**. Verbatim caption **"Consolidated gold sales,
net"** appears in both the 10-Q MD&A (*Results of Consolidated Operations*) and the 8-K.

| | 2026Q1 | 2021Q2 |
|---|---|---|
| Consolidated gold sales, net | **6,036** | **2,630** |
| Total Sales | 7,307 | 3,065 |

Two independent routes tie exactly. The accounting fact that makes the second route exact
(FY25-10K, *By-product Metals*): *"Revenues from by-product sales are credited to Costs applicable
to sales… Aside from the co-product sales at Cadia, Boddington, Penasquito, Red Chris, and Telfer,
copper and silver produced at other Newmont sites are by-product metals."* By-product revenue never
enters Sales, so at every non-co-product mine **segment Sales = gold Sales**.
Sum of gold-labelled + non-co-product mine rows: 2026Q1 = 6,036 ✓ · 2021Q2 = 2,630 ✓
Same identity holds for CAS (1,610 / 1,091) and D&A (489 / 469).

Note 5 *SALES* is the ASC 606 disaggregation, by mine AND product. Note 4/3 *Segment Information*
extends the metal split to CAS and D&A. **No derivation from price is needed anywhere in 2021-2026.**

XBRL caveat: the Note 5 table is inline-XBRL tagged, but there is **no XBRL fact for consolidated
gold revenue** — the MD&A table is untagged. Extraction must parse the MD&A/8-K table or sum
segment rows under the co-product-mine rule.

## Caption map

| GAIM term | Verbatim caption | Location | 2026Q1 | 2021Q2 |
|---|---|---|---|---|
| segment_revenue_gold | "Consolidated gold sales, net" | MD&A *Results of Consolidated Operations* | 6,036 | 2,630 |
| opcost_ex_dda | "Costs applicable to sales" (fn: excludes D&A and reclamation) | P&L; gold rows of segment note | gold 1,610 | gold 1,091 |
| segment_dda | "Depreciation and amortization" | P&L / segment note | gold 489 | gold 469 |
| royalties_production_taxes | "Royalties and Production Taxes" — **$/oz, ANNUAL only** | 10-K Item 2 *Production Costs per Ounce Sold* | null (FY25 $142/oz) | null (FY21 $61/oz) |
| corporate_g_and_a | "General and administrative" | P&L | 79 (gold 67) | 64 (gold 46) |
| exploration_total | "Exploration" + "Advanced projects, research and development" — **two P&L lines** | P&L | 51+45 = 96 | 52+37 = 89 |
| capex_total | "Additions to property, plant and mine development" | CF investing | 641 | **814 is 6-mo**; discrete Q2 = 415 |
| reclamation_accretion | "Reclamation accretion" / "Remediation accretion" | Reclamation & Remediation note | 72 / 2 | 30 / 3 |
| lease_payments | "Payments on lease and other financing obligations" | CF financing | 27 | 36 (6-mo); discrete 18 |
| net_interest | "Interest expense, net of capitalized interest" − "Interest income" | P&L; Other income note | **−45 (net income)** | 65 |
| cash_tax_paid | CF fn "cash payments for income and mining taxes, net of refunds" | CF footnote | 1,268 | **NOT_DISCLOSED** |
| gold_oz_sold | "Consolidated gold ounces (thousands): Sold" / "Attributable … Sold" | 10-Q highlights | 1,232,000 / 1,211,000 | 1,444,000 / 1,383,000 |
| published_aisc | 10-Q "All-in sustaining costs: Gold (per ounce)" = **co-product**; 8-K "Total Gold AISC per ounce (by-product)" | both | **1,709 co / 1,029 by** | **1,035 co / 918 by** |

## Segment structure changed twice, with recasts

| Period | Reportable segments |
|---|---|
| 2019Q2–2022Q4 | 5 geographic (North America, South America, Australia, Africa, Nevada) |
| 2023Q1 | **13 — by mine.** *"Segment results for the prior periods have been recast."* |
| 2023Q4 | 18 (post-Newcrest, recast again) |
| 2024 → 2026 | 17 → 14 → 12 → **13** (divestiture programme) |

Mitigation: the 2021–2022 10-Qs voluntarily disclosed mine-level rows anyway — *"the Company
internally reports information on a mine-by-mine basis… and has chosen to disclose this
information"* — so Sales/CAS/D&A per mine are continuous 2021→2026. But **region-level aggregates
die at 2022Q4**, and **2021 quarters were never recast** into the mine structure (only FY2021 was).

## Traps requiring a cross-company ruling

| # | Trap | Impact |
|---|---|---|
| T1 | `cash_tax_paid` quarterly footnote first appears **2025Q1**. Before that, annual only. | Kills ~17 of 21 quarters. Contract has no `ANNUAL_ONLY` flag. |
| T2 | `royalties_production_taxes` is annual, **per-ounce**, never a $ amount. Granularity changed by-region (FY21) → by-mine (FY25). Royalties sit inside CAS. | Converting to $ requires multiplying by ounces — a derivation. |
| T4 | `net_interest` = **−45** in 2026Q1 (interest income 84 > expense 39, on an $8.8bn cash balance). | Contract says costs positive. This is real economics, not a sign error. Capitalised interest is annual-only. |
| T5 | **Two published AISC per quarter, 78% apart** (co 1,709 / by 1,029), and the headline basis flipped to by-product in 2026. Newmont's "co-product" is a hybrid — by-product credits ($153) are still netted inside CAS. | Tolerance gate must be applied against the matching basis. |
| T6 | Co-product allocation uses a **fixed annual GEO price deck**, reset each year (2021: gold $1,200; 2026: gold $4,000), and its mine coverage widened. | Gold CAS/oz jumps at every year boundary for non-mining reasons. |
| T9 | **"Total Reportable Segments" ≠ Consolidated.** Divested (CC&V, Musselwhite, Éléonore) and held-for-sale mines sit outside it. | Reading the wrong row understates 2025Q1 revenue by 320 (6.4%). Always read `Consolidated`. |
| T10 | Attributable basis exists for **ounces only**. Revenue, CAS, D&A, capex, AISC are **consolidated only**. | METHODOLOGY §2 mandates attributable. Newmont cannot supply it. Flag `ONLY_CONSOLIDATED` on every observation. |
| T11 | **NGM is proportionately consolidated at 38.5%**; Barrick consolidates NGM 100% with a 38.5% NCI. | Structurally non-comparable between our two largest companies, permanently. Disclose, cannot fix. |
| T12 | Unit drift: silver "7,615" (thousand oz, 2021) vs "10" (million oz, 2026), same table. | 762x parser trap — the koz/Moz failure mode already logged in this project. |
| T14 | Reclamation ambiguity: P&L 78, accretion 72, but AISC keeps only 33 operating accretion + 27 ARC amortisation, excluding 41 at closed sites. | `Reclam_Au` is ambiguous between 72, 60 and 33+27. |
| T3 | Q2/Q3 cash-flow statements are **year-to-date**. | `derived_from_cumulative=true` mandatory. For capex prefer the segment-note footnote (*"capital expenditures on a cash basis were $415"*) over subtraction; no such footnote exists for leases or taxes. |
| T8 | 2021 has discontinued operations (650 total = 640 continuing + 10 discontinued); revenue 3,065 is continuing-only. | L0b must pin to continuing operations to avoid mixing bases. |

## Observed in-sample: the by-product pathology

Mine-level by-product AISC goes deeply negative where by-products dominate —
**Peñasquito −$9,318/oz**, **Red Chris −$1,117/oz**, **Cadia −$139/oz** — exactly the failure
mode METHODOLOGY §5 predicts. Newmont is **coverage tier 2**; non-gold revenue rose from
14.2% of Sales (2021Q2) to 17.4% (2026Q1) on the silver rally, so the by-product/co-product
uncertainty band widens across the window.

No non-calendar periods, no currency issues, no restatements of amounts.
