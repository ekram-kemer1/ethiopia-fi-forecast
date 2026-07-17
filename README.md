# Ethiopia Financial Inclusion Forecasting

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

- **Source dataset:** `data/raw/ethiopia_fi_unified_data.csv` — unified schema where
  `record_type` (`observation` / `event` / `impact_link` / `target`) determines how
  to interpret each row. See `data/raw/reference_codes.csv` for valid categorical values.
- **Enrichment:** additions beyond the starter dataset are documented, with sources,
  in `data/data_enrichment_log.md`.

## Branching / PR workflow

    task-1 -> PR -> main
    task-2 -> PR -> main
    task-3 -> PR -> main
    task-4 -> PR -> main
    task-5 -> PR -> main