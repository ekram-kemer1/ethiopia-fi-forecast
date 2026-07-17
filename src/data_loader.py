"""Shared data-loading utilities for the Ethiopia FI Forecasting project.

Used by notebooks and the Streamlit dashboard so the unified-schema loading
logic (and its validation against reference_codes.csv) lives in one place.
"""
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

DATA_FILE = RAW_DIR / "ethiopia_fi_unified_data.csv"
REF_FILE = RAW_DIR / "reference_codes.csv"

CATEGORICAL_FIELDS = [
    "record_type", "category", "pillar", "indicator_direction", "value_type",
    "source_type", "confidence", "gender", "location", "relationship_type",
    "impact_direction", "impact_magnitude", "evidence_basis",
]


def load_unified_data(path: Path = DATA_FILE) -> pd.DataFrame:
    """Load the unified schema dataset (observations, events, impact_links, targets)."""
    df = pd.read_csv(path)
    df["observation_date"] = pd.to_datetime(df["observation_date"], errors="coerce")
    return df


def load_reference_codes(path: Path = REF_FILE) -> pd.DataFrame:
    """Load valid categorical (field, code) pairs."""
    return pd.read_csv(path)


def validate_schema(df: pd.DataFrame, ref: pd.DataFrame) -> dict:
    """Return {field: [invalid values]} for any categorical value not in reference_codes."""
    violations = {}
    for field in CATEGORICAL_FIELDS:
        if field not in df.columns:
            continue
        valid_codes = set(ref.loc[ref["field"] == field, "code"])
        actual = df[field].dropna()
        actual = actual[actual != ""]
        bad = sorted(set(actual) - valid_codes)
        if bad:
            violations[field] = bad
    return violations


def get_observations(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["record_type"] == "observation"].copy()


def get_events(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["record_type"] == "event"].copy()


def get_impact_links(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["record_type"] == "impact_link"].copy()


def get_targets(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["record_type"] == "target"].copy()