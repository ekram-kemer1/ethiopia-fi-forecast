"""Shared forecasting logic for Ethiopia FI Forecasting project.

Extracted from notebooks/task4_forecasting.ipynb so the dashboard (Task 5) and
notebook stay in sync rather than duplicating the calibrated model inline.
"""
import pandas as pd

# Fit in Task 3 by calibrating the raw additive event-indicator association
# matrix against the observed 2021-2024 Access change (46% -> 49%).
ACCESS_CALIBRATION_FACTOR = 0.153


def event_effect(as_of_date, event_date, lag_months, full_effect):
    """Linear ramp from 0 (at event_date) to full_effect (at event_date + lag_months),
    held constant after that. Returns 0 before the event."""
    if pd.isna(event_date) or pd.isna(full_effect) or as_of_date < event_date:
        return 0.0
    months_elapsed = (as_of_date.year - event_date.year) * 12 + (as_of_date.month - event_date.month)
    if pd.isna(lag_months) or lag_months <= 0:
        return full_effect
    fraction = min(months_elapsed / lag_months, 1.0)
    return fraction * full_effect


def build_links_full(links: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
    return links.merge(
        events[["record_id", "indicator", "observation_date"]]
            .rename(columns={"record_id": "parent_id", "indicator": "event_name", "observation_date": "event_date"}),
        on="parent_id", how="left"
    )


def calibrated_event_effect_at(date, acc_links: pd.DataFrame, calibration_factor: float = ACCESS_CALIBRATION_FACTOR) -> float:
    raw = sum(
        event_effect(date, row["event_date"], row["lag_months"], row["impact_estimate"])
        for _, row in acc_links.iterrows()
    )
    return raw * calibration_factor


def access_scenarios(access: pd.DataFrame, links_full: pd.DataFrame, years=(2025, 2026, 2027)) -> pd.DataFrame:
    """Returns a DataFrame indexed by year with pessimistic/base/optimistic Access forecasts."""
    acc_links = links_full[links_full["related_indicator"] == "ACC_OWNERSHIP"]

    a24 = access[access["observation_date"].dt.year == 2024]["value_numeric"].iloc[0]
    a21 = access[access["observation_date"].dt.year == 2021]["value_numeric"].iloc[0]
    recent_slope = (a24 - a21) / (2024 - 2021)
    recent_trend = {yr: a24 + recent_slope * (yr - 2024) for yr in years}

    effect_end_2024 = calibrated_event_effect_at(pd.Timestamp("2024-12-31"), acc_links)

    scenarios = {}
    for yr in years:
        effect_at_yr = calibrated_event_effect_at(pd.Timestamp(f"{yr}-12-31"), acc_links)
        incremental = effect_at_yr - effect_end_2024
        base = recent_trend[yr] + incremental
        raw_incr = incremental / ACCESS_CALIBRATION_FACTOR if ACCESS_CALIBRATION_FACTOR else 0
        optimistic = recent_trend[yr] + raw_incr * 0.40
        pessimistic = recent_trend[yr]
        scenarios[yr] = {"pessimistic": pessimistic, "base": base, "optimistic": optimistic}

    out = pd.DataFrame(scenarios).T
    out.index.name = "year"
    return out


def usage_proxy_scenarios(usage_proxy: pd.DataFrame, years=(2025, 2026, 2027)) -> pd.DataFrame:
    """Returns a DataFrame indexed by year with pessimistic/base/optimistic Usage-proxy forecasts.
    Usage proxy = Mobile Money Account Rate (ACC_MM_ACCOUNT); no direct 'digital
    payment adoption' series exists in the dataset - see README/data_enrichment_log.md."""
    u21 = usage_proxy[usage_proxy["observation_date"].dt.year == 2021]["value_numeric"].iloc[0]
    u24 = usage_proxy[usage_proxy["observation_date"].dt.year == 2024]["value_numeric"].iloc[0]
    slope = (u24 - u21) / (2024 - 2021)

    scenarios = {}
    for yr in years:
        yrs_ahead = yr - 2024
        base = u24 + slope * yrs_ahead
        optimistic = u24 + slope * 1.5 * yrs_ahead
        pessimistic = u24 + slope * 0.5 * yrs_ahead
        scenarios[yr] = {"pessimistic": pessimistic, "base": base, "optimistic": optimistic}

    out = pd.DataFrame(scenarios).T
    out.index.name = "year"
    return out