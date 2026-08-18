# Round 1 Discovery + Extraction — Kinross Gold (KGC), CIK 0000701818

IFRS, USD, foreign private issuer (6-K quarterly / 40-F annual). Periods worked in full:
**2026Q2** and **2021Q2**; all 22 quarters 2021Q1–2026Q2 extracted to
`data/interim/KGC_quarterly.csv`. Parsed from local files with BeautifulSoup/lxml. No WebFetch.
No margin computed. Money USD **millions** (Kinross reports in millions — no unit conversion
needed anywhere). Ounces absolute troy ounces. Costs positive.

---

## 0. HEADLINE: Kinross is a **gold-equivalent-ounce reporter that calls it co-product**

This is the single most important finding and it changes Kinross's tier.

Kinross's headline cost metrics are **per gold *equivalent* ounce**. Its own verbatim definition
(2026Q2 press release, *Attributable Production Cost of Sales per Ounce Sold on a By-Product Basis*):

> "Attributable production cost of sales per ounce sold on a by-product basis is a non-GAAP ratio
> which calculates the Company's non-gold production as a credit against its per ounce production
> costs, **rather than converting its non-gold production into gold equivalent ounces and crediting
> it to total production, as is the case in co-product accounting.**"

— i.e. **Kinross explicitly labels its own gold-equivalent presentation "co-product accounting."**
Identical wording appears in the 2021Q2 press release, so this is stable across the whole window.

And it is mathematically true. Converting silver ounces at the spot price ratio and adding them to
the denominator is *algebraically identical* to allocating joint cost on relative revenue:

```
GEO cost/oz = C / (Au_oz + Ag_oz / r)        where r = P_Au / P_Ag
co-product  = C · Rev_Au/(Rev_Au+Rev_Ag) / Au_oz = C / (Au_oz + (P_Ag/P_Au)·Ag_oz)   ≡ same
```
Verified 2026Q2: 486,507 Au oz + 771,000 Ag oz / 61.61 = 499,021 vs published 499,035 GEO sold ✓

**So, unlike Barrick and Agnico (§5 open item), Kinross DOES publish a genuine co-product
restatement — it just calls the ounces "gold equivalent."** It publishes both conventions side by
side in every quarter, so the by-product/co-product wedge is directly observable, e.g. 2026Q2
AISC **1,821 co-product/GEO vs 1,751 by-product** ($70/oz, 4.0%); 2021Q2 **1,069 vs 1,048**.

### But the allocation factor is a spot price ratio that swings violently
Kinross footnote: *"'Gold equivalent ounces' include silver ounces produced and sold converted to a
gold equivalent based on a ratio of the average spot market prices for the commodities for each
period."* Observed ratio by quarter: 68.33 → 68.05 → 73.45 → 71.51 → 78.19 → 82.76 → 89.91 → 82.90
→ 83.82 → 81.88 → 81.82 → 83.13 → 88.70 → 81.06 → 84.06 → 84.67 → 89.69 → **97.41** → 87.73 → 76.34
→ **57.79** → 61.61. That is a **68% swing in four quarters** (97.41 in 2025Q2 → 57.79 in 2026Q1).
This is exactly the METHODOLOGY §5 "GEO embeds a price ratio that drifts" hazard, and it is the
reason `gold_oz_produced`, `aisc_denominator_oz`, `published_aisc` and `published_aic` all carry
`GEO_BASIS` in the CSV.

### Tier ruling requested
The contamination is small — **silver is 0.59%–5.91% of Metal sales (mean 2.84%)** over 2021Q1–2026Q2.
That is Tier 1 territory in magnitude but Tier 3-style in *construction* for the ounce-denominated
metrics. My recommendation: **Tier 1 for the revenue-share metric (GAIM), with `GEO_BASIS` on every
observation**, because `segment_revenue_gold` is a clean gold-only dollar figure (see §2) and never
touches the GEO conversion. The GEO contamination is confined to the ounce columns and the published
AISC/AIC checksums.

**METHODOLOGY §5 correction:** the presentation table says "Kinross | By-product | Silver netted",
and the brief cited "~8% of metal sales per a 2013 SEC comment letter". Both are wrong for
2021–2026: the **headline is gold-equivalent (co-product)**, by-product is the secondary
presentation, and silver never reaches 6% of Metal sales in the window.

---

## 1. Caption map — 2026Q2 and 2021Q2, verbatim, with values

Primary source (MD&A **and** interim condensed financial statements in ONE exhibit):
* 2026Q2 `data/raw/KGC/2026-Q2_0001104659-26-088237_tm2621038d1_ex99-1.htm`
* 2021Q2 `data/raw/KGC/2021-Q2_0000701818-21-000012_ex99-1.htm`

Checksum source (press release):
* 2026Q2 `data/raw/KGC/2026-Q2_0001171843-26-005026_exh_991.htm`
* 2021Q2 `data/raw/KGC/2021-Q2_0001104659-21-097160_tm2123587d1_ex99-1.htm`

| CSV field | Verbatim caption | Statement / section | 2026Q2 | 2021Q2 |
|---|---|---|---|---|
| total_revenue | `Metal sales` | Interim Condensed Consolidated Statements of Operations | 2,238.1 | 1,000.9 |
| segment_revenue_gold | `Metal sales - as reported` − `Less: silver revenue (c)` (2026); `Metal sales` − `Less: attributable (b) silver revenue (c)` (2021) | MD&A §11 non-GAAP recon / IS | **2,181.1** | **973.5** |
| opcost_ex_dda | `Production cost of sales` | IS | 674.7 | 460.0 |
| segment_dda | `Depreciation, depletion and amortization` | IS | 275.5 | 225.8 |
| royalties | — **no line item exists**, royalties sit inside Production cost of sales (narrative only) | — | null | null |
| corporate_g_and_a | `General and administrative` | IS | 32.4 | 31.4 |
| exploration_expensed | `Exploration and business development` | IS | 39.1 | 34.0 |
| — of which exploration only | MD&A prose: *"Included in total exploration and business development expense are expenditures on exploration totaling $29.0 million…"* | MD&A §5 | 29.0 | 28.6 |
| capitalised_exploration | MD&A prose: *"Capitalized exploration expenses, including capitalized evaluation expenditures, totaled $19.1 million…"* | MD&A §5 | **not disclosed after 2025Q1** | 19.1 |
| capex_total | `Additions to property, plant and equipment` | Statements of Cash Flows, Investing | 411.0 | 205.4 |
| reclamation_accretion | `Accretion of reclamation and remediation obligations` | MD&A §5 Finance expense table = FS Note 5iv | 11.9 | 3.5 |
| lease_payments | `Payment of lease liabilities` | CF, Financing | 2.0 | 8.0 |
| net_interest | `Interest expense, including accretion of debt and lease liabilities` − `Finance income` | MD&A §5 Finance expense table; IS | 8.4 − 19.8 = **−11.4** | 16.5 − 1.7 = **+14.8** |
| cash_tax_paid | `Income taxes paid` | CF, Operating (below `Cash flow provided from operating activities`) | 326.9 | 42.2 |
| gold_oz_sold | `Gold ounces sold` | MD&A §11 by-product recon | 486,507 | 536,681 |
| gold_oz_produced | `Produced` under `Total gold equivalent ounces` — **GEO, not gold** | MD&A §1 highlights | 501,341 | 541,954 |
| aisc_denominator_oz | `Attributable (a) gold equivalent ounces sold` | MD&A §11 GEO AISC recon | 490,240 | 547,819 |
| published_aisc | `Attributable (a) all-in sustaining cost per equivalent ounce sold` | MD&A §11 | 1,821 | 1,069 |
| published_aic | `Attributable (a) all-in cost per equivalent ounce sold` | MD&A §11 | 2,404 | 1,376 |
| published_aisc_byproduct | `Attributable (a) all-in sustaining cost per ounce sold on a by-product basis` (2021: `Attributable (b) …`) | MD&A §11 by-product recon | 1,751 | 1,048 |
| published_aic_byproduct | `Attributable (a) all-in cost per ounce sold on a by-product basis` (2021: `Attributable (b) …`) | MD&A §11 by-product recon | 2,348 | 1,364 |
| byproduct_credits | `Less: attributable (a) impact of silver by-product (n)` (2026) / `Less: attributable (b) silver revenue (c)` (2021) | MD&A §11 by-product recon | 56.2 | 27.4 |
| net_income_attributable | `Net earnings attributable to common shareholders` | MD&A §1 highlights = IS | 844.2 | 119.3 |

AISC build-up components used for `recon_aisc` (all in the same §11 table, verbatim captions):
`Production cost of sales - as reported`, `Less: non-controlling interest (b) production cost of
sales` (2021: `Less: portion attributable to Chirano non-controlling interest (a)`),
`General and administrative (f)`, `Other operating expense - sustaining (g)`,
`Reclamation and remediation - sustaining (h)`, `Exploration and business development - sustaining (i)`,
`Additions to property, plant and equipment - sustaining (j)`, `Lease payments - sustaining (k)`.

```
2026Q2  (674.7 − 19.8) + 32.4 + 4.8 + 23.5 + 15.7 + 159.7 + 1.8 = 892.8 / 490,240 = 1,821.1  vs 1,821  (+0.008%)
2021Q2  (460.0 −  5.4) + 31.4 + 3.5 + 10.1 +  9.1 +  69.2 + 7.9 = 585.8 / 547,819 = 1,069.3  vs 1,069  (+0.031%)
```
**All 22 quarters reconcile within ±0.036%** — max |residual| 0.036%, far inside the 2% gate.
`NO_AISC_CHECK` is set on zero observations: Kinross publishes AISC **and AIC**, on **both** GEO and
by-product bases, in every one of the 22 quarters. (Contrast Barrick, which dropped AIC after 2024Q2.)

### Independent cross-check that does not reuse the AISC table
`segment_revenue_gold / gold_oz_sold` reproduces Kinross's published
`Average realized gold price per ounce` (defined by Kinross as *"gold revenue divided by total gold
ounces sold"*) to **within ±0.05% in all 22 quarters** (e.g. 2026Q2 4,484.8 vs 4,483; 2021Q2 1,813.9
vs 1,814). This proves both the gold-revenue derivation and the discrete-quarter column choice.

---

## 2. Gold vs other-metal revenue — a clean gold-only figure DOES exist

**There is NO IFRS 15 revenue-disaggregation-by-metal note.** The income statement carries a single
line, `Metal sales`; the segment note (IFRS 8) disaggregates `Metal sales` **by mine only**, never by
metal. The gold/silver split lives **exclusively in the MD&A §11 non-GAAP reconciliations.**

Two regimes:

| Period | What is published | Basis |
|---|---|---|
| **2024Q4 – 2026Q2** | A dedicated table: `Metal sales - as reported` → `Less: silver revenue (c)` → `Less: non-controlling interest (b) gold revenue` → **`Attributable (a) gold revenue`** | attributable gold revenue is a **stated line** (2026Q2: 2,144.3) |
| **2021Q1 – 2024Q3** | Only `Less: silver revenue` / `Less: attributable silver revenue` inside the by-product cost recon | gold revenue must be obtained as `Metal sales` − `silver revenue` |

I used **consolidated gold revenue = `Metal sales` − `silver revenue`** in all 22 quarters for
homogeneity — taking the pair from the dedicated gold-revenue reconciliation where it exists
(2024Q4+, consolidated `Less: silver revenue`) and from the by-product cost reconciliation before
that. Note the two silver figures are NOT identical after 2024Q4: 2026Q2 `Less: silver revenue`
57.0 (consolidated) vs `Less: attributable impact of silver by-product` 56.2 (attributable) — the
gap is the Manh Choh NCI. `segment_revenue_gold` uses the former; `byproduct_credits` records the
latter, because that is the credit Kinross actually nets in its by-product cost metric (it also matches the consolidated basis of every cost column). This is a subtraction of
two stated line items, **never price × ounces**, and it is validated by the realised-price tie-out
above. The 2024Q4+ attributable figure is 1.5–1.7% lower (2026Q2: 2,144.3 attributable vs 2,181.1
consolidated); it is carried in this note, not in the CSV, to avoid a mid-series basis break.

**Is it GEO? No — the revenue figure is genuinely gold-only.** Silver revenue is removed in dollars,
not converted. GEO contamination in Kinross is confined to the *ounce* columns. So `NO_SEGMENT_SPLIT`
is **not** set on any observation, and the numerator of GAIM is clean.

Caption drift worth flagging: the deduction was captioned **`Less: attributable silver revenue`** and
described as *"Revenue from the sale of silver … effectively reduces the cost of gold production"*
through 2024Q3; from 2024Q4 it is **`Less: attributable impact of silver by-product`**, redefined as
*"the **costs allocated** to the production of secondary or by-product metal"*. The number did not
change character — 2026Q2 silver revenue 57.0 vs "impact of silver by-product" 56.2, the gap being
exactly the NCI share — so it is still revenue-netting wearing a cost-allocation label. Do not read
the new caption as a genuine cost allocation.

---

## 3. Segment structure, discontinued operations and restatements

Reportable segments read off the IFRS 8 note header row in each quarter:

| Quarter | Operating segments | Non-operating |
|---|---|---|
| 2021Q1–Q3 | Fort Knox, Round Mountain, Bald Mountain, Paracatu, **Kupol**, Tasiast, **Chirano** | Corporate and other |
| 2022Q1 | Fort Knox, Round Mountain, Bald Mountain, Paracatu, Tasiast, **Chirano** | **Great Bear** (acq. 24 Feb 2022), Corporate and other |
| 2022Q2 | Fort Knox, Round Mountain, Bald Mountain, Paracatu, Tasiast | Great Bear, Corporate and other |
| 2022Q3–2023Q1 | + **La Coipa** (restart) | Great Bear, Corporate and other |
| 2023Q2 → 2026Q2 | Tasiast, Paracatu, La Coipa, Fort Knox, Round Mountain, Bald Mountain | Great Bear, Corporate and other |

* **Kupol/Dvoinoye (Russia)** — removed from continuing operations at **2022Q1**; sold 2022.
* **Chirano (Ghana, 90%)** — still in continuing operations in the 2022Q1 filing, moved to
  discontinued operations in the **2022Q2** filing; sold Aug 2022.
* **Manh Choh (70%)** — from **2024Q1** the Fort Knox segment "includes Manh Choh"; this creates the
  30% NCI that all "attributable" measures adjust for. Before 2022 the only NCI was Chirano (10%);
  **2022Q2–2023Q4 there is effectively no NCI deduction in the AISC tables at all.**
* **Segment ORDER changed at 2023Q2** (Fort Knox-first → Tasiast-first) with no change of content —
  a pure position-parsing trap. Segment note number moved 13 → 12.

### Quarters carrying discontinued-operations presentation
**2022Q1 through 2023Q3** (17 to 48 occurrences of "discontinued operations" each; from 2023Q4
onward only residual tax/legal references). Flag `DISCONTINUED_OPS_PRESENTATION` in the CSV.
In those filings revenue and net income are split onto two bases and both appear in the same tables.

### The restatement, quantified
2021 as **originally** filed (total operations) vs as **recast** in the 2022 filings (continuing
operations only), `Metal sales`:

| | 2021Q1 | 2021Q2 | 2021Q3 | 2021Q4 | FY2021 |
|---|---|---|---|---|---|
| as originally reported | 986.5 | 1,000.9 | 862.5 | 879.5 | 3,729.4 |
| recast, continuing ops | 694.4 | 707.9 | 582.4 | 614.9 | 2,599.6 |
| net earnings attrib. — original | 149.5 | 119.3 | (44.9) | (2.7) | 221.2 |
| net earnings attrib. — continuing | 79.1 | 30.1 | (72.9) | (66.2) | (29.9) |

(recast source: `2022-Q2_0000701818-22-000007_ex99-1.htm`, MD&A §7 *Summary of Quarterly
Information*, footnote *"The quarterly results were updated retrospectively to reflect the impact of
Chirano and Russian discontinued operations."*)

**2022Q1 was restated again within 2022** when Chirano moved to discontinued operations:

| line (2022Q1) | as originally filed | restated in 2022Q2 filing | delta |
|---|---|---|---|
| Metal sales | 768.0 | 700.9 | −67.1 |
| Production cost of sales | 410.6 | 363.1 | −47.5 |
| Depreciation, depletion and amortization | 180.8 | 166.5 | −14.3 |
| Exploration and business development | 24.8 | 23.4 | −1.4 |
| Additions to property, plant and equipment | 106.3 | 100.7 | −5.6 |
| Income taxes paid | 83.9 | 82.4 | −1.5 |
| Accretion of reclamation and remediation | 4.8 | 4.0 | −0.8 |
| General and administrative / Payment of lease liabilities | 30.2 / 5.4 | 30.2 / 5.4 | 0.0 |

**CSV convention: each row is as reported in that period's own filing.** 2021 rows are therefore
total-operations; 2022Q1 is Chirano-in-continuing; 2022Q2 onward are continuing-operations. Rows
affected carry `RESTATED`. Consequence, verified: the four discrete quarters sum **exactly** to the
published full year for 2021, 2023, 2024 and 2025 on every extracted line, and are off by exactly the
2022Q1 deltas above for 2022. Rebasing 2021 onto continuing operations is a downstream decision — the
recast numbers are in the table above; I did not improvise it.

**Trap inside a single table:** the 2022 highlights table carries `Total gold equivalent ounces`
(541,954 for 2021Q2 — total ops) directly above `Financial Highlights from Continuing Operations`
`Metal sales` (707.9 — continuing only). Dividing one by the other produces nonsense.

---

## 4. Cumulative vs discrete — **Kinross needs almost no derivation**

This is where Kinross differs most from Newmont/Barrick/Agnico, and it is good news.

**The interim condensed consolidated statements of OPERATIONS, COMPREHENSIVE INCOME and CASH FLOWS
all present a discrete THREE-MONTH column alongside the six/nine-month column.** Column headers read
`Three months ended | Six months ended` (or `Nine months`) with a year row beneath. So capex, income
taxes paid, lease payments and every P&L line are **discrete for Q1, Q2 and Q3 with no subtraction**.

Column selection rule actually used (header text, never position): a table qualifies only if its
header block matches `Three months`; the column index is then derived from the **year header row**
(e.g. `2026 | 2025 | Change | % Change | 2026 | 2025 | Change | % Change` → 8 value columns, first
group = three months, index 0). Two independent implementations (header-derived column map, and
first-numeric-cell) were run against each other on every field in every quarter and **agree in 100%
of cases**. Note the 4-column and 8-column layouts coexist *in the same document* — MD&A §5 tables
carry Change/%Change, MD&A §11 and the financial statements do not.

**Q4 (`derived_q4`)** — the annual filing's statements are 12-month only, but **the Q4 press release
carries a discrete `Three months ended December 31,` column** for the highlights table, the gold
revenue reconciliation, both cost reconciliations (full AISC *and* AIC build-ups) and the
sustaining/non-sustaining capex table. So for Q4 these are read directly, not derived:
`total_revenue, opcost_ex_dda, segment_dda, capex_total, net_income_attributable, gold_oz_sold,
gold_oz_produced, aisc_denominator_oz, published_aisc, published_aic, byproduct_credits`, and all
AISC build-up components.

Only these eight are derived as **FY − 9M** (9M read from the Q3 filing's nine-month column, itself
header-asserted): `corporate_g_and_a, exploration_expensed, reclamation_accretion, net_interest`
(both legs), `cash_tax_paid, lease_payments, capitalised_exploration`.
Verification: FY − 9M − (Q1+Q2+Q3) = 0.0 on every field for 2021, 2023, 2024, 2025; 2025 capex
1,194.2 FY − 826.0 9M = 368.2 = the press-release Q4 figure, exactly.

Fields that are **year-to-date-only and therefore genuinely lost**: none.

---

## 5. Non-overlap rulings (METHODOLOGY §13 Rule 1) — checked against Kinross specifically

**Finance expense IS a gross bundle, but Kinross disaggregates it.** MD&A §5 / FS Note 5iv:
```
Interest expense, including accretion of debt and lease liabilities   8.4
Accretion of reclamation and remediation obligations                 11.9
Finance expense                                                      20.3
```
So `net_interest` is built from the **`Interest expense, including accretion of debt and lease
liabilities`** line (NOT the `Finance expense` total) minus `Finance income`, and
`reclamation_accretion` is taken from the separate accretion line. **Exhaustive and non-overlapping;
neither is null.** Taking `Finance expense` as the interest line would have double-charged accretion
— that is the Agnico failure mode and Kinross would have reproduced it.

**Capitalised exploration is inside capex.** Kinross says so verbatim, footnote (h):
*"'Additions to property, plant and equipment – sustaining' represents the majority of capital
expenditures at existing operations **including capitalized exploration costs**, periodic capitalized
stripping and underground mine development costs…"* Therefore `exploration_expensed` is the P&L line
only and `capitalised_exploration` is a **diagnostic column, never subtracted**.

**Lease payments.** Footnote (k): *"'Lease payments – sustaining' represents the majority of lease
payments as reported on the interim condensed consolidated statements of cash flows and is made up of
the **principal and financing components** of such cash payments."* CF `Payment of lease liabilities`
= sustaining + non-sustaining exactly (2026Q2 2.0 = 1.8+0.2; 2021Q2 8.0 = 7.9+0.1; FY2021 33.8 =
32.8+1.0). So `lease_payments` already carries both components. Residual overlap: the P&L interest
line includes *accrual* accretion of lease liabilities (~$0.2–0.3M/quarter on a $16–20M lease
liability) — immaterial, flagged not adjusted.

**`net_interest` is signed and goes negative.** 2025Q3 −27.1, 2026Q1 −8.2, 2026Q2 −11.4 — Kinross
now runs $2.7bn of cash against $0.74bn of senior notes, so finance income exceeds interest expense.
Not clamped, not flipped.

---

## 5b. The two AISC columns, and which one the AISC-margin cross-check must use

`published_aisc` / `published_aic` are **per gold-EQUIVALENT ounce** (Kinross's headline,
co-product-equivalent, denominator `aisc_denominator_oz`).
`published_aisc_byproduct` / `published_aic_byproduct` are **per gold ounce sold** (denominator is
gold ounces only, silver netted out of the cost). Both are published in **all 22 quarters**; there
are no nulls.

**Use the by-product pair for the METHODOLOGY §4b AISC-margin cross-check.** That cross-check divides
gold revenue by *gold* ounces sold, so the per-GEO figure is a basis mismatch: its denominator
contains silver converted at a spot ratio that moved 97.41:1 → 57.79:1 in four quarters, which drags
the margin with the silver price rather than with mining economics. Measured effect of the mismatch:

| | mean | min | max |
|---|---|---|---|
| `published_aisc_byproduct` (per gold oz) | **$1,351.3/oz** | 953 (2021Q1) | 1,781 (2025Q4) |
| `published_aisc` (per GEO oz) | $1,379.8/oz | 975 | 1,825 |
| wedge (GEO − by-product) | **$28.5/oz = 2.11%** | $4 (2022Q1) | $75 (2026Q1) |
| `published_aic_byproduct` (per gold oz) | $1,715.6/oz | 1,279 | 2,348 |

AISC margin `(realised px − AISC)/realised px`, computed from CSV columns as
`segment_revenue_gold*1e6/gold_oz_sold`:

* **by-product (correct basis): mean 41.90%, range 26.75% (2022Q3) → 66.00% (2026Q1)** — monotone in
  the gold price, no silver artefacts.
* per-GEO (mismatched basis): mean 40.76%. **Using the GEO figure understates the AISC margin by
  1.13 points on average, and by 1.9 points in the worst quarter (2022Q4/2023Q1).**

One basis caveat, quantified rather than assumed: the by-product AISC denominator caption itself
drifts — `Attributable gold ounces sold` (2021Q1–2022Q1 and 2024Q3–2026Q2) vs consolidated
`Gold ounces sold [from continuing operations]` (2022Q2–2024Q2, the interval with no NCI). The CSV's
`gold_oz_sold` is consolidated throughout. Where Kinross publishes both realised prices they differ
by at most **0.089%**, which moves the AISC margin by at most **0.042 percentage points** — below any
threshold that matters. Recorded, not adjusted.

## 6. Conflicts with the methodology / contract — reported, not patched

1. **§5 presentation table is wrong for Kinross** (see §0): headline is gold-equivalent
   (co-product by Kinross's own definition), not by-product; silver is ≤5.91%, not ~8%.
2. **§2 mandates an attributable basis; Kinross cannot supply a fully attributable row.** It
   publishes attributable versions of only five things: gold revenue (2024Q4+), production cost of
   sales, capital expenditures, ounces sold, and the AISC/AIC ratios. DD&A, G&A, exploration, finance
   income/expense, income taxes paid and lease payments are **consolidated only**. I set
   `basis=consolidated` and `ONLY_CONSOLIDATED` on every row and kept the whole row on one basis
   rather than mixing. The *checksum* internals (production cost of sales net of NCI, attributable
   GEO ounces) are attributable, because the published AISC/AIC they tie to are attributable — that
   is stated here rather than hidden. NCI is small: 10% of Chirano pre-2022, 30% of Manh Choh
   from 2024Q1.
3. **`exploration_expensed` has no clean caption. — RULED, closed.** The P&L line is
   `Exploration and business development`; there is no separate exploration line on any statement.
   The exploration-only figure exists **only as MD&A prose** and its definition drifted:
   "expenditures on exploration" (2021, and again 2025Q1+) → "expenditures on exploration **and
   technical evaluations**" (2022Q2–2024Q4) → back. **Coordinator ruling: use the P&L line; do not
   carve out business development from prose whose definition moves.** Applied. Every row carries
   `EXPL_INCL_BUSINESS_DEV`; the eleven quarters 2022Q2–2024Q4 whose narrow prose definition included
   "and technical evaluations" additionally carry `EXPL_CAPTION_DRIFT`.
4. **`royalties` is never disclosed as an amount** — it is inside `Production cost of sales` and
   appears only in narrative ("higher royalty costs as a result of the higher average realized gold
   price"). Null in all 22 quarters, exactly as Newmont's CAS. Same comparability trap as
   Barrick, whose royalties *are* a separate line.
5. **Capitalised interest is excluded from `net_interest` and from `capex_total`. — RULED, closed.**
   The cash flow statement shows `Interest paid capitalized to property, plant and equipment` as a
   **separate investing line** from `Additions to property, plant and equipment` (2021Q2 7.8; 2026Q2
   7.1 for the six months; 2025Q2 17.0). METHODOLOGY §2 says net interest should include capitalised
   interest. **Coordinator ruling: leave it in neither column — putting it in either would break the
   non-overlap rule — and make the omission visible.** Applied: every row carries `CAPINT_EXCLUDED`.
   (Accrual capitalised interest is also disclosed in Note 5iv footnote (a): $7.4M for 2026Q2.)
6. **`capitalised_exploration` disclosure stopped after 2025Q1.** Prose figures exist 2021Q1–2025Q1
   (2021Q4/2022Q4/2023Q4/2024Q4 derived FY − 9M); null + `NOT_DISCLOSED:capitalised_exploration`
   from 2025Q2. Values used: 12.7, 19.1, 22.5, 20.8 / 8.1, 10.9, 11.2, 14.6 / 15.5, 22.5, 25.7, 29.7
   / 22.7, 27.0, 24.0, 18.4 / 11.0, –, –, –.
7. **Flag vocabulary gaps. — `DISCONTINUED_OPS_PRESENTATION` and `derived_q4` GRANTED.** Also in
   use, pending ratification: `CAPINT_EXCLUDED`, `EXPL_INCL_BUSINESS_DEV`, `EXPL_CAPTION_DRIFT`, and
   the qualified `NOT_DISCLOSED:<field>` forms.
8. **`gold_oz_produced` holds gold-EQUIVALENT ounces produced.** Kinross publishes **no gold-only
   production figure anywhere** — production is GEO in the highlights, the operating statistics and
   the per-mine operating summary. Recorded with `GEO_BASIS` rather than dropped; `gold_oz_sold` is
   genuinely gold-only. Do not compute a gold-only recovery or production-vs-sales ratio from it.

---

## 7. File anatomy and further traps

| Exhibit | Content |
|---|---|
| `…_6k.htm` | 6-K cover only |
| big exhibit (0.6–4.6 MB), title *"FINANCIAL STATEMENTS AND MD&A"* or *"management's discussion and analysis"* | **PRIMARY** — MD&A **and** interim condensed FS + notes, in ONE file (Q1–Q3) |
| second exhibit, title *"NEWS RELEASE"/"PRESS RELEASE"* | **CHECKSUM** — earnings release |
| Q4 6-K | MD&A `ex99-1` (annual, no discrete Q4) **and** audited FS `ex99-2`; the Q4 **press release** is the only source with discrete Q4 columns |
| 40-F | `ex99-1` AIF, `ex99-2` FY MD&A, `ex99-3` audited FS — duplicates of the Q4 6-K content, filed ~6 weeks later |

* **Filer-agent switch at 2025Q4**: press releases move from accession prefix `0001104659-…`
  (`tm…_ex99-1.htm`) to `0001171843-…` (`exh_991.htm`). File-name-pattern matching breaks there.
* **Three different capex numbers in one filing (2026Q2)**: cash flow `Additions to property, plant
  and equipment` **411.0**; MD&A §6 capex-by-segment total **411.0** (same, cash basis); IFRS 8 note
  `Capital expenditures … (c)` **488.4** — footnote (c): *"Segment capital expenditures are presented
  on an accrual basis and include capitalized interest."* Plus `Attributable capital expenditures`
  406.2. Reading the segment note would overstate capex by 19%.
* **Legacy annual tables sit inside quarterly MD&As**: 2022Q2 §11 contains a `Years ended December
  31, 2021 | 2020` AISC reconciliation immediately after the quarterly ones. Any caption match that
  does not assert `Three months` in the header will grab FY2021 numbers into a 2022Q2 row.
* **Cell-splitting artefact**: percentage-change cells split as `(20` + `)%` across two `<td>`s in
  some 2023 tables, shifting every later cell by one. Merge `)`/`)%` fragments into the previous cell
  before mapping columns, or the nine-month column is silently mis-read.
* **A `-` (nil) cell in the three-month column shifts a first-numeric parser onto the six-month
  value.** Real example, 2026Q2 CF: `Interest paid capitalized to property, plant and equipment |
  Note 7 | - | - | (7.1) | (13.5)` — a naive parser returns 7.1 (six months) as the quarter. None of
  the extracted fields hit this, but it is one caption away.
* **G&A in the AISC build-up ≠ G&A on the income statement** in some quarters (2022Q3: 27.3 vs 40.3;
  2023Q3: 24.0 vs 25.8) — footnote (f): *"…excluding certain impacts which the Company believes are
  not reflective of the Company's underlying performance."* The CSV column takes the **income
  statement** line; the reconstruction takes the AISC line, which is why the two must not be
  conflated.
* **AISC caption drops "Attributable" for 2022Q2–2023Q4** (`All-in sustaining cost from continuing
  operations per equivalent ounce sold`) while the AIC caption keeps it — in the same table.
* Kinross reports **in millions with one decimal**, never thousands. No unit conversion anywhere; no
  koz/Moz ambiguity in the financial tables (silver ounces sold are printed in 000's in the
  highlights table only — `Silver ounces - sold (000's)` 771 = 771,000 oz).

---

## 8. Coverage

22 of 22 quarters extracted, 32 columns. Zero rejected. Zero `NO_AISC_CHECK`. Zero
`NO_SEGMENT_SPLIT`. `published_aisc_byproduct` and `published_aic_byproduct` populated 22/22.
Empty cells: `royalties` (22/22, genuinely not disclosed) and `capitalised_exploration` (5/22,
disclosure discontinued after 2025Q1). Everything else is populated and reconciles.
