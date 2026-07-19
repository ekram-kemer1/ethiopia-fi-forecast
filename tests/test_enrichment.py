import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data_loader import load_unified_data, get_observations, get_events, get_impact_links

NEW_RECORD_IDS = ["REC_0034", "REC_0035", "EVT_0011", "IMP_0015", "IMP_0016"]


def test_enrichment_record_count():
    """Enrichment should add exactly 5 records: 57 base -> 62 total."""
    df = load_unified_data()
    assert len(df) == 62, f"Expected 62 records after enrichment, found {len(df)}"


def test_all_new_records_present():
    df = load_unified_data()
    present = set(df["record_id"]) & set(NEW_RECORD_IDS)
    missing = set(NEW_RECORD_IDS) - present
    assert not missing, f"Missing enriched records: {missing}"


def test_new_records_have_required_provenance_fields():
    """Every new record must document who collected it, when, and from where."""
    df = load_unified_data()
    new_rows = df[df["record_id"].isin(NEW_RECORD_IDS)]
    for _, row in new_rows.iterrows():
        assert row["collected_by"], f"{row['record_id']} missing collected_by"
        assert row["collection_date"], f"{row['record_id']} missing collection_date"
        assert row["confidence"] in ("high", "medium", "low"), \
            f"{row['record_id']} has invalid confidence: {row['confidence']}"


def test_new_observations_have_source_url():
    """New observation records must cite a checkable source."""
    df = load_unified_data()
    new_obs = df[df["record_id"].isin(["REC_0034", "REC_0035"])]
    for _, row in new_obs.iterrows():
        assert row["source_url"], f"{row['record_id']} missing source_url"
        assert row["source_url"].startswith("http"), \
            f"{row['record_id']} source_url is not a valid link"


def test_new_impact_links_flagged_as_theoretical():
    """IMP_0015/IMP_0016 have no empirical Ethiopia-specific data yet and
    must be explicitly marked theoretical, not overstated as empirical."""
    df = load_unified_data()
    new_links = df[df["record_id"].isin(["IMP_0015", "IMP_0016"])]
    for _, row in new_links.iterrows():
        assert row["evidence_basis"] == "theoretical", \
            f"{row['record_id']} evidence_basis should be 'theoretical', got {row['evidence_basis']}"


def test_event_pillar_left_blank_by_design():
    """EVT_0011, like all events, should NOT have pillar pre-assigned -
    effects belong in impact_link rows only."""
    df = load_unified_data()
    evt = df[df["record_id"] == "EVT_0011"].iloc[0]
    assert evt["pillar"] == "" or str(evt["pillar"]) == "nan", \
        "EVT_0011 should not have a pillar assigned directly"