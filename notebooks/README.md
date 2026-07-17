# Notebooks

Run in order — each task builds on the enriched dataset from Task 1.

| Notebook | Task | Description |
|---|---|---|
| `task1_data_exploration_enrichment.ipynb` | 1 | Schema exploration, reference-code validation, dataset enrichment summary |
| `task2_eda.ipynb` | 2 | Exploratory data analysis: temporal coverage, Access/Usage trends, event timeline, correlations |
| `task3_impact_modeling.ipynb` | 3 | Event–indicator association matrix, impact model, validation vs. historical data |
| `task4_forecasting.ipynb` | 4 | Access & Usage forecasts 2025–2027 with confidence intervals and scenarios |

Notebooks are paired with jupytext `.py` (percent format) companions of the same
name for readable diffs in PRs. Edit either file and re-pair with:

```bash
jupytext --sync notebooks/task1_data_exploration_enrichment.ipynb
```

All notebooks assume they are run from inside `notebooks/` (relative paths like
`../data/raw/...`).