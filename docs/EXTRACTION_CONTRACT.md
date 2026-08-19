# Extraction Contract v0.2 — binding on every extraction agent

This document removes discretion. Where it and METHODOLOGY.md disagree, this one wins for
extraction mechanics; METHODOLOGY.md wins for what the metric means.

**If a rule here does not fit what you actually see in a filing, do NOT improvise. Report the
conflict to the main agent. A rule that bends per-agent is not a rule.**

## A. Universal conventions

| Convention | Rule |
|---|---|
| Currency | **USD millions**, 3 decimals. Pilot 6 all report in USD — if you find otherwise, STOP and report. Never use an external FX source; if translation is needed use the rate the filing itself discloses. |
| Ounces | **Troy ounces, absolute** (1,232,000 — not "1,232 koz", not "1.232 Moz"). The koz/Moz confusion has already produced one dimensionally impossible figure in this project. |
| Signs | **All cost and outflow items entered POSITIVE.** The formula subtracts them. Never enter a cost as negative. |
| Basis | **Attributable**, not consolidated. If the filing gives only consolidated, record it, set `basis="consolidated"`, and flag `ONLY_CONSOLIDATED`. Record both when both are given. |
| Ounces measure | **SOLD**, never produced. Agnico Eagle reports per ounce *produced* — you must locate ounces *sold*. If only produced is available, flag `ONLY_PRODUCED` and record it in a separate field; do not silently substitute. |
| Period | Calendar quarter. **Q4 is derived as FY − Q1 − Q2 − Q3** wherever only cumulative figures are published; set `derived_q4=true`. |
| Half-yearly filers | Record as `2025H1` / `2025H2`. **Never split a half into two quarters.** Never interpolate. |
| Cumulative figures | Many 6-K releases give year-to-date, not discrete-quarter, figures (Agnico Q3 2025 capex was 9-month cumulative). Derive the discrete quarter by subtraction and set `derived_from_cumulative=true`. If the prior period is unavailable, flag `ONLY_CUMULATIVE` and leave the discrete field null. |
| Rounding | Record what the filing states. Do not re-round, do not "clean up". |

## B. Provenance — mandatory on every single number

No figure enters the dataset without all four:
```json
{"value": 1234.5,
 "src_file": "data/raw/NEM/2026-Q1_0001164727-26-000017_nem-20260331.htm",
 "src_statement": "Condensed Consolidated Statements of Operations",
 "src_caption": "Costs applicable to sales"}
```
`src_caption` must be the **verbatim caption as printed in the filing**, not your paraphrase.
This is what lets the audit team re-verify without re-reading the whole document. An agent that
cannot cite the caption did not read the statement.

## C. Flag vocabulary — three machine-read families, plus open documentation

**v0.2 correction.** This section used to say "closed set, do not invent new codes."
That was never true in practice and is not the right rule. **68 distinct descriptive
codes are in active use** that this document never defined, and most carry information
no generic code could (`SUKARI_CONSOLIDATED_100PCT_AGA_OWNS_50PCT`,
`H2_AISC_TABLE_DISCLOSED_IN_NEXT_H1_RELEASE`). Suppressing them would destroy
provenance to satisfy a rule nothing enforced.

The workable distinction is not open-vs-closed, it is **read-vs-descriptive**.

### C.1 Machine-read flags — exactly three families, spelling is load-bearing

| Flag | What reads it | What happens if you misspell it |
|---|---|---|
| `TIER<A\|AEQ\|B\|C\|D>:<field>[:<code>]` | `build_series.grade_fidelity` | The regex does not match, the position silently falls back to its default tier, and the row grades **as if you never wrote the flag** |
| `CAT2_SUBSTITUTION` | headline-aggregate cap | The row silently stays in the headline aggregate |
| `CAPINT_INCLUDED_IN_CAPEX` | capitalised-interest add-back | Capitalised interest is silently added twice |

`<field>` must be one of the twelve names in `FIDELITY_FIELDS` (DEGRADATION §9.1).
**`src/build_series.py:validate_flags` now checks all three** and reports unparseable
tier flags, tier flags naming a non-existent field, and near-miss spellings of the two
literals. Before that check existed, every one of these failed silently — a correction
that looks applied and isn't is worse than no correction.

### C.2 Descriptive flags — open, but they are a record, not a shrug

Anything else is documentation for a human reader. Write them freely, but:
- **UPPER_SNAKE_CASE**, and specific enough to be re-checkable a year later.
- A descriptive flag never substitutes for a machine-read one. If a line is bundled,
  `ROYALTIES_IN_OPCOST` is a fine note but `TIERAEQ:royalties:BUNDLED_IN_OPCOST` is
  what actually stops the build treating it as a silent zero-fill. **Write both.**
- Prefer an existing code over a synonym — grep the interim CSVs before coining one.

### C.3 The originally-defined codes (all still valid)

| Flag | Meaning |
|---|---|
| `NOT_DISCLOSED` | The line genuinely is not in the filing. Value stays null. **Never estimate.** |
| `ONLY_CUMULATIVE` | Year-to-date only, prior period unavailable for subtraction |
| `ONLY_CONSOLIDATED` | Attributable basis not given |
| `ONLY_PRODUCED` | Ounces produced given, ounces sold not |
| `NO_SEGMENT_SPLIT` | Gold cannot be separated from other metals in this filing |
| `GEO_BASIS` | Figure is gold-EQUIVALENT, contaminated by other metals (Gold Fields) |
| `NO_AISC_CHECK` | Company does not publish AISC for this period, checksum skipped |
| `ALLOCATION_SENSITIVE` | Corporate-overhead convention changes the margin by >1.5 points |
| `RESTATED` | Filing restates a prior period — record both the original and restated value |

## D. Output schema — one JSON file per company-period

`data/interim/<TICKER>_<PERIOD>.json`. Fixed keys. Null where not disclosed — never zero,
never a guess. **Zero and null are different claims and must not be conflated.**

```json
{
  "ticker": "NEM", "cik": "0001164727", "period": "2026Q1",
  "period_start": "2026-01-01", "period_end": "2026-03-31",
  "basis": "attributable", "currency": "USD", "report_frequency": "quarterly",

  "L0_inputs": {
    "segment_revenue_gold": {...}, "segment_cost_of_sales": {...},
    "segment_dda": {...}, "net_income_attributable": {...}, "total_revenue": {...}
  },
  "L1_inputs": {
    "opcost_ex_dda": {...}, "royalties_production_taxes": {...},
    "corporate_g_and_a": {...}, "exploration_total": {...},
    "capex_total": {...}, "reclamation_accretion": {...},
    "lease_payments": {...}, "net_interest": {...},
    "cash_tax_paid": {...}, "one_off_items": {...}, "nci_share": {...}
  },
  "checksum_inputs": {
    "gold_oz_sold": {...}, "realised_gold_price": {...},
    "published_aisc": {...}, "published_aic": {...},
    "sustaining_capex": {...}, "growth_capex": {...},
    "byproduct_credits": {...}, "aisc_basis": "by-product|co-product|GEO"
  },
  "flags": [], "notes": "", "coverage_tier": 1
}
```

## E. Per-company line mapping — TO BE FILLED BY ROUND 1

Round-1 agents fill their own row from the ACTUAL filings. Do not guess from another
company's captions — the whole point of this table is that they differ.

| GAIM term | NEM | GOLD/B | AEM | AU | KGC | GFI |
|---|---|---|---|---|---|---|
| segment_revenue_gold | | | | | | |
| opcost_ex_dda | | | | | | |
| segment_dda | | | | | | |
| royalties_production_taxes | | | | | | |
| corporate_g_and_a | | | | | | |
| exploration_total | | | | | | |
| capex_total | | | | | | |
| reclamation_accretion | | | | | | |
| lease_payments | | | | | | |
| net_interest | | | | | | |
| cash_tax_paid | | | | | | |
| gold_oz_sold | | | | | | |
| published_aisc | | | | | | |

Known starting points (verified, still confirm against the filing):
- **NEM** anchors AISC on "Costs applicable to sales"; **GOLD** anchors on "Cost of sales".
  They are NOT the same line. This is a first-order comparability trap.
- **AEM** publishes both by-product and co-product reconciliations, per ounce **produced**.
- **GFI** reports gold-**equivalent** ounces (Cerro Corona copper, Salares Norte silver ~4%).
- **NEM** does not state gold revenue in the earnings release — it is in the 10-Q revenue
  disaggregation note. Do not derive it as price x ounces.

## F. Validation gate — an observation is admissible only if

1. Every non-null figure carries full provenance (§B).
2. Reconstructed AISC ties to published AISC within **2%**, or `NO_AISC_CHECK` is set with a reason.
3. `segment_revenue_gold` came from a statement, not a multiplication.
4. Units pass a magnitude sanity check: revenue in USD millions 100–10,000; ounces 100,000–3,000,000
   per quarter; realised price within 50–200% of the same company's prior quarter.
5. No flag is `NO_SEGMENT_SPLIT` for a Tier-1 company (that would mean we misread the filing).

Failing observations go to `data/interim/rejected/` with the reason. **Rejected is a valid
outcome and must be reported. Silently dropping an observation is not.**
