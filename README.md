# Ethiopia Financial Inclusion Forecasting
![Tests](https://github.com/ekram-kemer1/ethiopia-fi-forecast/actions/workflows/unittests.yml/badge.svg)
**10 Academy KAIM 9 — Week 11 Challenge**
Forecasting Access (Account Ownership) and Usage (Digital Payment Adoption) for
Ethiopia, 2025-2027, using a unified events/observations/impact-links schema.

## Project Structure

ethiopia-fi-forecast/
├── .github/workflows/      # CI (unit tests on push/PR)
├── data/
│   ├── raw/                # ethiopia_fi_unified_data.csv, reference_codes.csv
│   ├── processed/          # analysis-ready outputs
│   └── data_enrichment_log.md
├── notebooks/               # Task 1-4 notebooks
├── src/                     # reusable python modules
├── dashboard/app.py         # Streamlit dashboard (Task 5)
├── tests/
├── models/                  # saved forecasting models / impact matrices
├── reports/figures/         # exported charts for the final report
├── requirements.txt
└── README.md

## Setup

    python -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\activate
    pip install -r requirements.txt

## Running the notebooks

    jupyter lab notebooks/

## Running the dashboard

    streamlit run dashboard/app.py

## Data

## Data

- **Source dataset:** `data/raw/ethiopia_fi_unified_data.csv` — unified schema where
  `record_type` (`observation` / `event` / `impact_link` / `target`) determines how
  to interpret each row. See `data/raw/reference_codes.csv` for valid categorical values.
- **Enrichment:** 5 records added beyond the starter dataset (2 observations, 1 event,
  2 impact_links). Every addition is fully documented — source URL, exact quoted text,
  field-by-field placement rationale, and explicit stated assumptions — in
  [`data/data_enrichment_log.md`](data/data_enrichment_log.md).

### Validation & Assumptions

Every record (base + enriched) is validated programmatically, not just visually:

| Check | Where |
|---|---|
| Every categorical field matches `reference_codes.csv` | `notebooks/task1_data_exploration_enrichment.ipynb`, Section 3 |
| All 5 enriched records present with required provenance fields | `tests/test_enrichment.py` |
| `impact_link.parent_id` always references a real event | `tests/test_data_loader.py::test_impact_links_have_valid_parent` |
| Theoretical (non-empirical) impact estimates explicitly flagged | `tests/test_enrichment.py::test_new_impact_links_flagged_as_theoretical` |

Run all checks locally with:
```bash
pytest tests/ -v
```

Known limitations and explicitly-stated assumptions behind each enrichment decision
are documented in [`data/data_enrichment_log.md`](data/data_enrichment_log.md) —
see "Data Limitations Identified" and the per-record "Assumption stated explicitly"
notes.

## Branching / PR workflow

    task-1 -> PR -> main
    task-2 -> PR -> main
    task-3 -> PR -> main
    task-4 -> PR -> main
    task-5 -> PR -> main