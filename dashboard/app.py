"""Ethiopia Financial Inclusion Forecasting Dashboard.

Run with:
    streamlit run dashboard/app.py

This is a Task 1 scaffold — Overview/Trends/Forecasts/Inclusion Projections
pages will be built out in Task 5 once forecasts (Task 4) are available.
"""
import sys
from pathlib import Path

import streamlit as st
import plotly.express as px

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data_loader import load_unified_data, get_observations, get_events

st.set_page_config(page_title="Ethiopia Financial Inclusion Forecast", layout="wide")

st.title("🇪🇹 Ethiopia Financial Inclusion Forecasting")
st.caption("Selam Analytics — 10 Academy KAIM 9, Week 11")

df = load_unified_data()
obs = get_observations(df)
events = get_events(df)

col1, col2, col3 = st.columns(3)
with col1:
    latest_access = obs[obs["indicator_code"] == "ACC_OWNERSHIP"].sort_values("observation_date").iloc[-1]
    st.metric("Account Ownership (latest)", f"{latest_access['value_numeric']}%",
              help=f"As of {latest_access['observation_date'].date()}")
with col2:
    latest_mm = obs[obs["indicator_code"] == "ACC_MM_ACCOUNT"].sort_values("observation_date").iloc[-1]
    st.metric("Mobile Money Account Rate (latest)", f"{latest_mm['value_numeric']}%",
              help=f"As of {latest_mm['observation_date'].date()}")
with col3:
    st.metric("Events Cataloged", len(events))

st.divider()
st.subheader("Account Ownership Trajectory (2011–2024)")
access_trend = obs[(obs["indicator_code"] == "ACC_OWNERSHIP") & (obs["gender"] == "all")]
fig = px.line(access_trend.sort_values("observation_date"), x="observation_date", y="value_numeric",
              markers=True, labels={"value_numeric": "Account Ownership (%)", "observation_date": "Date"})
st.plotly_chart(fig, use_container_width=True)

st.info(
    "This is the Task 1 scaffold. Trends, Forecasts, and Inclusion Projections "
    "pages will be added in Task 5 (see project Tasks 2-4 for the underlying analysis)."
)

st.download_button(
    "Download unified dataset (CSV)",
    df.to_csv(index=False),
    file_name="ethiopia_fi_unified_data.csv",
    mime="text/csv",
)