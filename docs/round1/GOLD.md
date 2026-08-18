# Round 1 Discovery — Barrick Mining Corp (GOLD / B), CIK 0000756894

Periods worked in full: **2026Q1** and **2021Q2**. USD millions. Costs positive.
Parsed from local files. No WebFetch. No margin computed. All arithmetic tie-outs reproduce
the filing's own totals exactly.

## File anatomy — corrects an assumption in the contract

Barrick does NOT file the press release and financial statements as separate exhibits:

| Exhibit | Content |
|---|---|
| `…d6k.htm` | 6-K cover only (carries inline XBRL in Q2/Q4 filings) |
| `…dex991.htm` | Press release — **CHECKSUM source** |
| `…dex992.htm` | MD&A **and** condensed interim financial statements + notes, in ONE file — **PRIMARY source** |

40-F: `dex991` = AIF, `dex993` = audited FS, `dex994` = FY MD&A.

## SETTLED: Barrick's "co-product" is gross-of-credits, not a reallocation

Barrick's own definition, verbatim:
> "Our co-product metrics remove the impact of other metal sales that are produced as a
> by-product of our gold production from cost per ounce calculations **but does not reflect a
> reduction in costs for costs associated with other metal sales.**"

Reproduced, 2021Q2: by-product credits 70 − NCI 30 = net 40; 40 / 1,070 koz = **$37/oz**, added
identically to TCC (729→766), AISC (1,087→1,124) **and** AIC (1,269→1,306). Same pattern 2025Q3:
credits 80 − NCI 28 = 52; 52/837 = **$62/oz**, added to TCC and AISC alike.

This is `AISC_gross = AISC_reported + credits/oz` — **step 2 of METHODOLOGY §5, not step 5.**
No joint cost is reallocated; no revenue weight is applied. **Barrick's co-product figure is not
comparable to Newmont's or Freeport's and must be used only as the credits gross-up input.**
METHODOLOGY §12 open item 1 is closed.

**Provenance upgrade:** by-product credits equal Note 6 `Other sales` in **11 of 11** periods
tested (FY2022-FY2025, Q1/Q4 2025, Q1/Q2 2026, Q2 2021, 6M 2021/2026). Source the credits from
the audited statements, not the non-GAAP table.

## CONFLICT: Barrick stopped publishing AIC after 2024Q2

METHODOLOGY §2 makes AIC the primary reconciliation anchor. Last AIC table and per-ounce value:
**Q2 2024**. From **Q3 2024** the table title drops to "…Total cash costs and All-in sustaining
costs…" with no AIC line. Zero AIC occurrences in FY2024 MD&A, all of 2025, the FY2025 40-F,
2026Q1 or 2026Q2. Co-product disclosure also ended after **Q3 2025**.

**RULING: where AIC is unpublished, fall back to AISC as the checksum and set `AIC_UNAVAILABLE`.
Never self-compute an AIC and treat it as a checksum — validating our own numbers against our own
numbers is circular.** The agent correctly refused to improvise this. Impact is contained because
in the corrected forward design AIC is only a checksum, never an input.

Trap: the Q3 2024 press release still carries stale AIC *definition* boilerplate in its endnotes
while the table has none — a text-grep will find AIC where no AIC exists.

## Three mutually inconsistent "gold revenue" figures, 2026Q1

| Figure | Basis | Source | Reconciled? |
|---|---|---|---|
| **4,756** | consolidated IFRS | Note 6 `Gold sales` | yes, ties to income statement |
| **3,607** | attributable non-GAAP | MD&A `Revenues - as adjusted` | yes, full bridge |
| 3,682 | attributable, region-summed | press-release Regional Summary | **no — $75M unexplained** |

The earlier reconnaissance quoted 3,682, the unreconciled one. The bridge:
`Sales 4,756 − NCI 1,591 + equity-method 446 (Kibali 341 + Porgera 105) − closure sites 13
+ treatment/refining 9 = 3,607`; 748 koz; $4,823/oz realised.

Gold/copper separation is clean at **Note 6** (Gold 4,756 / Copper 343 / Other 119 = 5,218 = IS)
and **Note 7** (Gold column 1,874). Note 5 segments are **minesites, not commodities**, and Note 5
minesite revenue **includes** by-products. Use Note 6, not Note 5, for the numerator.

## The royalty double-count trap

Barrick's `Site operating costs` (1,179) **excludes** royalties; `Royalty expense` 193 and
`Mining and production taxes` 46 are separate Note 7 lines. Newmont's `Costs applicable to sales`
(1,610) **includes** royalties and never discloses them quarterly. Applying one GAIM rule to both
either under-counts Barrick by $239M or double-counts Newmont. This is the second-order half of
the anchor trap (Barrick anchors AISC on `Cost of sales`, Newmont on `Costs applicable to sales`).
There is **no separate royalty line in Barrick's AISC build-up** — it is already inside the 1,874 anchor.

## Kibali: the basis inconsistency in Barrick's own published metric

Kibali (45%) and Porgera (24.5%) are equity-accounted. Note 5 shows them as segments, then removes
them via an explicit `Share of equity investees` line. **Zero Kibali revenue reaches consolidated
revenue** — it appears only as `Income from equity investees`.

But Barrick's published AISC denominator, `Ounces sold - attributable basis` (748 koz), **includes**
Kibali and Porgera, while its consolidated cost of sales (1,874) **excludes** them. Any GAIM built
on consolidated revenue over attributable ounces is dimensionally wrong. Under §2's attributable
mandate, the `Revenues - as adjusted` bridge is the only self-consistent numerator for Barrick.

NCI is disclosed **as prose inside a Note 5 footnote**, not as a column — machine-hostile.

## Traps

| # | Trap |
|---|---|
| T1 | Statements show **4 columns**: 3M-current, 3M-**prior-year**, 6M-current, 6M-prior. Gate: 6M-current must equal Q1+Q2 (2026: 5,218+5,292=10,510 ✓). Picking column 3 doubles the quarter. |
| T1b | MD&A non-GAAP tables show **5 columns** where column 2 is the **sequential prior quarter**, not prior-year. Same document, two meanings of "column 2". |
| T1c | **Inline XBRL exists only in Q2 and Q4 filings** — verified across all 125 files. Q1/Q3 have zero. Half the quarterly series is unreachable via XBRL; HTML parsing is mandatory. |
| T4 | Caption drift: `Ounces sold - equity basis`→`- attributable basis` (2023Q3, both strings present in 2023Q4); anchor `Cost of sales applicable to gold production`→`COS applicable to gold production` (2025Q1, quarterlies only); `By-product credits`→`Costs allocated to by-products` (2025Q4, value unchanged, old caption survives on the copper page). |
| T5 | Press release embedded condensed statements only 2022Q2–2025Q2. |
| T6 | Name/ticker change sits **inside the 2025Q1 filing** ("Name and Ticker Change" section): Barrick Gold → Barrick Mining, NYSE GOLD → B effective 2025-05-09. Flag `BARRICK_TICKER_2025` at **2025Q1**, not Q2. CIK unchanged. |
| T7 | Unexplained segment-vs-consolidated revenue gap: `Other revenue` **(55)** in 2026Q1, **+24** in 2021Q2. Sign not fixed, no explanation given. Record as-is; do not net into gold. |
| T8 | Q4 has a discrete 3-month column so `derived_q4=false` — but the AISC recon's 3-month columns are sequential (12/31/25 | 9/30/25) while FY columns are annual (12/31/25 | 12/31/24 | 12/31/23). Five columns, two meanings of "12/31/25". Highest-risk table in the series. |
| — | Ounces published **only in koz** — every Barrick ounce figure is rounded to the thousand. Flag accordingly. |

Segment change: **Q1 2023** — Lumwana added as a reportable segment, Veladero removed, prior
periods restated. Note number moved 5 → 4 → 5 across the window.
Coverage tier: **2** at group level; Tier 1 only if confined to Note 6 Gold + Note 7 Gold column.
