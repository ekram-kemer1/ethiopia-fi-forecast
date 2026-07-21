import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data_loader import load_unified_data, get_observations, get_events, get_impact_links
from src.forecasting import build_links_full, access_scenarios, usage_proxy_scenarios


def _load():
    df = load_unified_data()
    obs = get_observations(df)
    events = get_events(df)
    links = get_impact_links(df)
    links_full = build_links_full(links, events)
    access = obs[(obs["indicator_code"] == "ACC_OWNERSHIP") & (obs["gender"] == "all")].sort_values("observation_date")
    usage_proxy = obs[(obs["indicator_code"] == "ACC_MM_ACCOUNT") & (obs["gender"] == "all")].sort_values("observation_date")
    return access, usage_proxy, links_full


def test_access_scenarios_shape():
    access, _, links_full = _load()
    scen = access_scenarios(access, links_full)
    assert list(scen.index) == [2025, 2026, 2027]
    assert set(scen.columns) == {"pessimistic", "base", "optimistic"}


def test_access_scenarios_ordering():
    """Pessimistic <= base <= optimistic must hold every year."""
    access, _, links_full = _load()
    scen = access_scenarios(access, links_full)
    for yr in scen.index:
        assert scen.loc[yr, "pessimistic"] <= scen.loc[yr, "base"] <= scen.loc[yr, "optimistic"]


def test_access_forecast_below_nfis_target():
    """Regression guard for the headline finding: even the optimistic 2025
    scenario should fall short of the 70% NFIS-II target."""
    access, _, links_full = _load()
    scen = access_scenarios(access, links_full)
    assert scen.loc[2025, "optimistic"] < 70


def test_usage_proxy_scenarios_shape():
    _, usage_proxy, _ = _load()
    scen = usage_proxy_scenarios(usage_proxy)
    assert list(scen.index) == [2025, 2026, 2027]
    assert set(scen.columns) == {"pessimistic", "base", "optimistic"}


def test_usage_proxy_scenarios_ordering():
    _, usage_proxy, _ = _load()
    scen = usage_proxy_scenarios(usage_proxy)
    for yr in scen.index:
        assert scen.loc[yr, "pessimistic"] <= scen.loc[yr, "base"] <= scen.loc[yr, "optimistic"]