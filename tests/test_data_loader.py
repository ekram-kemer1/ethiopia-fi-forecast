import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data_loader import (
    load_unified_data, load_reference_codes, validate_schema,
    get_observations, get_events, get_impact_links, get_targets,
)


def test_data_loads():
    df = load_unified_data()
    assert not df.empty
    assert "record_type" in df.columns


def test_reference_codes_load():
    ref = load_reference_codes()
    assert not ref.empty
    assert {"field", "code"}.issubset(ref.columns)


def test_schema_is_valid():
    df = load_unified_data()
    ref = load_reference_codes()
    violations = validate_schema(df, ref)
    assert violations == {}, f"Schema violations found: {violations}"


def test_record_type_split_sums_to_total():
    df = load_unified_data()
    n = (len(get_observations(df)) + len(get_events(df))
         + len(get_impact_links(df)) + len(get_targets(df)))
    assert n == len(df)


def test_impact_links_have_valid_parent():
    df = load_unified_data()
    events = set(get_events(df)["record_id"])
    links = get_impact_links(df)
    assert links["parent_id"].isin(events).all(), "Some impact_links reference a missing event"