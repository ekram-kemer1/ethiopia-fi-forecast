# Data Enrichment Log

**Project:** Ethiopia Financial Inclusion Forecasting
**Collected by:** Ekram Kemer
**Collection date:** 2026-07-17
**Base file:** `data/raw/ethiopia_fi_unified_data.csv` (converted from the provided
`ethiopia_fi_unified_data.xlsx`, sheets `ethiopia_fi_unified_data` + `Impact_sheet`,
merged into one unified-schema table with `record_type` distinguishing rows).

Starting counts: 30 observation / 10 event / 14 impact_link / 3 target (57 records).
Ending counts: 32 observation / 11 event / 16 impact_link / 3 target (62 records).

---

## Enrichment Methodology

Additions were selected against three criteria, applied in order:

1. **Fills a named gap, not a random addition.** Each new record maps to a gap
   identified during Task 1 exploration (see `notebooks/task1_data_exploration_enrichment.ipynb`,
   Section 8): sparse enabler coverage (electricity, smartphones), and an
   uncatalogued 2024 regulatory event with plausible Access/Usage effects.
2. **Source credibility tier.** Preferred order: primary government/regulator data
   (World Bank, NBE, Parliament record) > industry-body research (GSMA) > news/legal
   commentary corroborating a primary event. All five additions meet this bar;
   none are sourced from unverified or single-source news.
3. **Schema conformance is checked, not assumed.** Every new record's categorical
   fields (`pillar`, `source_type`, `confidence`, `record_type`,
   `relationship_type`, `impact_direction`, `impact_magnitude`, `evidence_basis`)
   were validated against `data/raw/reference_codes.csv` programmatically — see
   "Validation" section below, not just visually checked.

## New Records Added

### 1. REC_0034 — Smartphone Adoption Rate (observation, ACCESS)
- **Value:** 40% (2023), projected 50% by 2030
- **Source:** GSMA, *The Mobile Economy Sub-Saharan Africa 2024*
- **Source URL:** https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-economy/wp-content/uploads/2024/11/GSMA_ME_SSA_2024_Web.pdf
- **Original text (quoted from source):** "Ethiopia Technology mix: 40% Smartphone
  adoption (2023), projected 50% by 2030"
- **Confidence:** high — primary industry-body report, single unambiguous figure,
  no conflicting estimate found in cross-checking (searched for a second source;
  none published at comparable rigor for Ethiopia specifically).
- **Field-by-field placement rationale:** `pillar=ACCESS` (not USAGE) because
  smartphone ownership is a precondition/enabler for using digital services, not
  a usage metric itself. `indicator_direction=higher_better` — more smartphones is
  unambiguously an enabler. `value_type=percentage`, `unit=%` — matches
  `reference_codes.csv` allowed values for this value_type.
- **Assumption stated explicitly:** treats "smartphone adoption" as distinct from
  `ACC_MOBILE_PEN` (mobile subscription penetration, 61.4%). This is a real
  distinction in the source (basic phones can hold a SIM without being a
  smartphone), not a duplicate indicator — flagged here so a reviewer doesn't
  mistake it for double-counting.

### 2. REC_0035 — Electricity Access Rate (observation, ACCESS)
- **Value:** 55.4% of population (2023); urban 94.7% / rural 43.6%
- **Source:** World Bank SDG7 / ESMAP Tracking SDG7 Electrification Database
- **Source URL:** https://data.worldbank.org/indicator/EG.ELC.ACCS.ZS?locations=ET
- **Original text (quoted from source):** "Access to electricity (% of population)
  in Ethiopia was reported at 55.4% in 2023"
- **Confidence:** high — World Bank official statistic, the standard reference
  series used for SDG7 tracking; internally consistent with prior-year WB releases.
- **Field-by-field placement rationale:** `pillar=ACCESS`, `indicator_direction=higher_better`.
  No `related_indicator` was set on this row (it is a plain observation, not an
  impact_link) — its relationship to Access outcomes is a hypothesis for Task 3
  correlation analysis, not an asserted causal claim, so it is intentionally
  NOT wired into `impact_link` yet.
- **Assumption stated explicitly:** the urban/rural split (94.7%/43.6%) is cited in
  `notes` but NOT entered as separate rows, because the dataset schema has no
  standing convention for a third `location` value beyond `national` used
  elsewhere for this indicator family — adding `urban`/`rural` rows here without
  a corresponding convention for other indicators would create an inconsistency.
  This is flagged as a **data gap**, not silently resolved.

### 3. EVT_0011 — Banking Business Proclamation No. 1360/2024 (event, category=regulation)
- **Date:** 2024-12-17 (Parliament approval)
- **Source:** Ethiopian Parliament, corroborated via Legal500 and independent law-firm
  publications (cross-checked across 3+ independent legal commentary sources
  before inclusion, since no single official parliamentary gazette URL was
  fetchable)
- **Source URL:** https://www.legal500.com/developments/thought-leadership/ethiopias-financial-sector-liberalization-the-new-banking-business-proclamation-and-its-implications/
- **Original text (quoted from source):** "On December 17, 2024, the Ethiopian
  Parliament approved the new Banking Business Proclamation No. 1360/2024,
  allowing foreign banks to re-enter the Ethiopian market after a 50-year absence."
- **Confidence:** high (multi-source corroboration), though note this is
  *secondary* reporting of a primary legal act, not the gazette text itself —
  disclosed here rather than overstated as a primary source.
- **Category chosen:** `regulation` (from `reference_codes.csv` valid `category`
  values for events) rather than `policy`, since this is a binding legal
  proclamation, not a strategy document (`policy` is used elsewhere for
  NFIS-II, which is a strategy, not a law) — this distinction was checked
  against how `category` was used on existing event rows before assigning it.
- **Design principle applied:** `pillar` is deliberately left blank on this row,
  consistent with every other event in the base dataset — its effects are
  captured only through `impact_link` rows (below), not asserted directly on
  the event.

### 4. IMP_0015 — EVT_0011 → ACC_OWNERSHIP (impact_link)
- **Direction/magnitude/lag:** increase / low (~+3pp) / lag 24 months
- **Evidence basis:** `theoretical` (not `empirical` or `literature`) — chosen
  deliberately because no Ethiopia-specific pre/post measurement exists yet
  (the event is 7 months old at time of writing) and the Nigeria comparator
  below is illustrative, not a rigorous natural-experiment match.
- **Why 24 months, why "low" not "medium":** foreign bank entry requires
  licensing, capital deployment, and branch/subsidiary setup — comparable
  liberalization episodes (Nigeria's 2000s consolidation/foreign entry) took
  1–3 years to show measurable effects on account ownership, and even then the
  effect size was modest relative to mobile-money-driven access gains. "Low"
  magnitude reflects that Ethiopia's binding constraint on Access appears (per
  Task 2 EDA) to be something other than product/branch supply — infrastructure
  enablers grew steadily while Access stagnated — so a supply-side intervention
  like foreign bank entry is not expected to be a large lever.
- **Explicit limitation:** `comparable_country=Nigeria` is a loose analogy
  (different banking structure, different starting account-ownership base) and
  should be treated as a directional prior for Task 3/4 scenario modeling, not
  a calibrated parameter — this caveat is repeated here deliberately since it is
  the single least certain record in the enrichment.

### 5. IMP_0016 — EVT_0011 → USG_DIGITAL_PAYMENT (impact_link)
- **Direction/magnitude/lag:** increase / negligible (~+1pp) / lag 30 months
- **Evidence basis:** `theoretical`
- **Why this link was still added despite being weak:** included for completeness
  of the event's impact surface (an event with only an Access-side impact_link
  would understate its downstream reach), but magnitude is deliberately set to
  `negligible` — the lowest value in `reference_codes.csv` for
  `impact_magnitude` — specifically so it does not carry disproportionate
  weight in any downstream aggregate impact score in Task 3.
- **Explicit limitation:** no source directly ties foreign bank entry to Ethiopian
  digital payment adoption; the rationale (foreign entrants bringing digital-first
  product design) is inference from general banking-liberalization literature,
  not Ethiopia-specific evidence — flagged as the weakest-evidence record in the
  dataset.

---

## Validation

Every new record was checked programmatically (not just visually) against
`reference_codes.csv` in `notebooks/task1_data_exploration_enrichment.ipynb`
(Section 3, "Schema validation"), which tests every categorical field on every
row — including the 5 new ones — against the reference code list and prints any
violation. Result at time of writing: **no violations found**, covering
`record_type`, `category`, `pillar`, `indicator_direction`, `value_type`,
`source_type`, `confidence`, `gender`, `location`, `relationship_type`,
`impact_direction`, `impact_magnitude`, `evidence_basis`.

Additionally checked:
- **Referential integrity:** both new `impact_link` rows (`IMP_0015`, `IMP_0016`)
  have `parent_id=EVT_0011`, which exists in the event table (tested in
  `tests/test_data_loader.py::test_impact_links_have_valid_parent`).
- **Record ID uniqueness:** `REC_0034`, `REC_0035` continue the observation ID
  sequence from `REC_0033`; `EVT_0011` continues from `EVT_0010`; `IMP_0015`/`IMP_0016`
  continue from `IMP_0014` — no ID collisions with the base 57 records.
- **No silent corrections:** the starter dataset's original 57 records were left
  untouched. No values were edited or overwritten during enrichment.

## Corrections
None. The starter dataset's existing 57 records were validated and no schema
violations, referential errors, or factual issues were found in them.

## Data Limitations Identified
- Only 5 Findex survey points span 13 years (2011, 2014, 2017, 2021, 2024) — sparse
  for time-series forecasting; this materially limits the reliability of any
  correlation/trend analysis in Task 2 (flagged again there) and forecasting in
  Task 4.
- Most events cluster in 2021–2025; earlier drivers of the 2011→2021 growth are
  not captured in the event log, so impact modeling can only explain the second
  half of the observed trajectory.
- Regional (sub-national) disaggregation is almost entirely absent — no
  urban/rural account-ownership split exists despite the newly-added electricity
  data suggesting a large urban/rural infrastructure gap could plausibly matter.
- The two new impact_link estimates (IMP_0015, IMP_0016) are theoretical/comparable-country
  based, not empirical — both are explicitly flagged above as the lowest-confidence
  records in the dataset and should be weighted accordingly (e.g. wide
  uncertainty bands, not point estimates) in Task 3/4 modeling.

## Suggested Next Additions (not yet added — flagged for future work)
- Findex 2024 urban/rural account ownership split (if available in Findex microdata)
- NBE agent count / mobile money agent density time series
- Ethiopia bank branch and ATM density time series (NBE Annual Reports)
- A second independent source for REC_0034 (smartphone adoption) to corroborate
  the single-source GSMA figure