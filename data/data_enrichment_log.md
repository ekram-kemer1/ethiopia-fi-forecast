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

## New Records Added

### 1. REC_0034 — Smartphone Adoption Rate (observation, ACCESS)
- **Value:** 40% (2023), projected 50% by 2030
- **Source:** GSMA, *The Mobile Economy Sub-Saharan Africa 2024*
- **Source URL:** https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-economy/wp-content/uploads/2024/11/GSMA_ME_SSA_2024_Web.pdf
- **Original text:** "Ethiopia Technology mix: 40% Smartphone adoption (2023), projected 50% by 2030"
- **Confidence:** high (primary industry-body report)
- **Why it's useful:** Smartphone ownership is a distinct enabler from basic mobile
  subscription penetration (already in the dataset as `ACC_MOBILE_PEN`). App-based
  mobile money features depend on smartphones, not just USSD-capable feature phones —
  relevant to both Access and Usage forecasting.

### 2. REC_0035 — Electricity Access Rate (observation, ACCESS)
- **Value:** 55.4% of population (2023); urban 94.7% / rural 43.6%
- **Source:** World Bank SDG7 / ESMAP Tracking SDG7 Electrification Database
- **Source URL:** https://data.worldbank.org/indicator/EG.ELC.ACCS.ZS?locations=ET
- **Original text:** "Access to electricity (% of population) in Ethiopia was reported
  at 55.4% in 2023"
- **Confidence:** high (World Bank official statistic)
- **Why it's useful:** Electricity access underpins agent-network uptime, POS/ATM
  operation, and device charging — a classic indirect enabler. Growth slowed from
  +0.77pp/yr (2010–2020) to +0.39pp/yr (2020–2023), mirroring the Access pillar's
  2021–2024 slowdown — worth testing as a candidate explanatory factor in Task 2/3.

### 3. EVT_0011 — Banking Business Proclamation No. 1360/2024 (event, category=regulation)
- **Date:** 2024-12-17 (Parliament approval)
- **Source:** Ethiopian Parliament, reported via Legal500 and multiple law firms
- **Source URL:** https://www.legal500.com/developments/thought-leadership/ethiopias-financial-sector-liberalization-the-new-banking-business-proclamation-and-its-implications/
- **Original text:** "On December 17, 2024, the Ethiopian Parliament approved the new
  Banking Business Proclamation No. 1360/2024, allowing foreign banks to re-enter the
  Ethiopian market after a 50-year absence."
- **Confidence:** high (corroborated by 6+ independent legal/news sources)
- **Why it's useful:** A major, previously-uncatalogued regulatory event — the first
  law permitting foreign bank participation in 50 years (caps aggregate foreign
  ownership at 49%). Per the unified schema's design principle, `pillar` is left
  blank on the event; its effects are captured through the two impact_links below.

### 4. IMP_0015 — EVT_0011 → ACC_OWNERSHIP (impact_link)
- **Direction/magnitude:** increase / low (~+3pp), lag 24 months
- **Evidence basis:** theoretical, comparable country Nigeria
- **Why:** Foreign entrants typically raise competition and branch/agent investment,
  but licensing and subsidiary set-up realistically take 1–2 years, so this is coded
  as an *enabling* (not direct) relationship with a substantial lag.

### 5. IMP_0016 — EVT_0011 → USG_DIGITAL_PAYMENT (impact_link)
- **Direction/magnitude:** increase / negligible (~+1pp), lag 30 months
- **Evidence basis:** theoretical
- **Why:** Coverage of Ethiopia's 2025 banking-sector deregulation shows incumbents
  investing in digital channels partly in response to competitive pressure; effect
  on digital payment usage is indirect and speculative — low confidence.

---

## Corrections
None — the starter dataset's existing 57 records were loaded and validated against
`reference_codes.csv` with no schema violations found (see Task 1 notebook,
"Schema validation" section).

## Data Limitations Identified
- Only 5 Findex survey points span 13 years (2011, 2014, 2017, 2021, 2024) — sparse
  for time-series forecasting.
- Most events cluster in 2021–2025; earlier drivers of the 2011→2021 growth are not
  captured in the event log.
- Regional (sub-national) disaggregation is almost entirely absent outside a couple
  of gender splits — no urban/rural account-ownership split, despite electricity
  data suggesting a large urban/rural gap could matter.
- New impact_link estimates (IMP_0015, IMP_0016) are theoretical/comparable-country
  based, not empirical — treat with appropriately wide uncertainty in Task 3/4.

## Suggested Next Additions
- Findex 2024 urban/rural account ownership split (if available in Findex microdata)
- NBE agent count / mobile money agent density time series
- Ethiopia bank branch and ATM density time series (NBE Annual Reports)