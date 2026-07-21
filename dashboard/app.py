##Imports and setup
"""Ethiopia Financial Inclusion Forecasting Dashboard.

Run with:
    streamlit run dashboard/app.py

Four pages: Overview, Trends, Forecasts, Inclusion Projections.
"""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data_loader import load_unified_data, get_observations, get_events, get_impact_links, get_targets
from src.forecasting import build_links_full, access_scenarios, usage_proxy_scenarios

st.set_page_config(page_title="Ethiopia Financial Inclusion Forecast", layout="wide", page_icon="\U0001F1EA\U0001F1F9")
# ---------- Load data once ----------
@st.cache_data
def get_data():
    df = load_unified_data()
    return df

df = get_data()
obs = get_observations(df)
events = get_events(df)
links = get_impact_links(df)
targets = get_targets(df)
links_full = build_links_full(links, events)

access = obs[(obs["indicator_code"] == "ACC_OWNERSHIP") & (obs["gender"] == "all")].sort_values("observation_date")
usage_proxy = obs[(obs["indicator_code"] == "ACC_MM_ACCOUNT") & (obs["gender"] == "all")].sort_values("observation_date")
# ---------- Sidebar navigation ----------
st.sidebar.title("\U0001F1EA\U0001F1F9 Ethiopia FI Forecast")
st.sidebar.caption("Selam Analytics \u2014 10 Academy KAIM 9, Week 11")
page = st.sidebar.radio("Go to", ["Overview", "Trends", "Forecasts", "Inclusion Projections"])
st.sidebar.divider()
st.sidebar.download_button(
    "\U0001F4E5 Download full dataset (CSV)",
    df.to_csv(index=False),
    file_name="ethiopia_fi_unified_data.csv",
    mime="text/csv",
)
# =====================================================================
# PAGE 1: OVERVIEW
# =====================================================================
if page == "Overview":
    st.title("Overview")
    st.caption("Key metrics and headline trend at a glance.")

    latest_access = access.iloc[-1]
    latest_mm = usage_proxy.iloc[-1]
    crossover = obs[obs["indicator_code"] == "USG_CROSSOVER"]["value_numeric"].iloc[0]
    access_2021 = access[access["observation_date"].dt.year == 2021]["value_numeric"].iloc[0]
    access_growth = latest_access["value_numeric"] - access_2021

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Account Ownership (latest)", f"{latest_access['value_numeric']:.0f}%",
               f"+{access_growth:.0f}pp since 2021", help=f"As of {latest_access['observation_date'].date()}, Global Findex")
    c2.metric("Mobile Money Account Rate", f"{latest_mm['value_numeric']:.1f}%",
               help=f"As of {latest_mm['observation_date'].date()}, Global Findex")
    c3.metric("P2P/ATM Crossover Ratio", f"{crossover:.2f}",
               help="P2P transactions now exceed ATM transactions (FY2024/25, EthSwitch)")
    c4.metric("Events Cataloged", len(events), help="Policies, product launches, infrastructure investments")

    st.divider()
    st.subheader("Account Ownership Trajectory (2014-2024)")
    fig = px.line(access, x="observation_date", y="value_numeric", markers=True,
                  labels={"value_numeric": "Account Ownership (%)", "observation_date": "Year"})
    fig.update_traces(line_color="#2a7f62", line_width=3, marker_size=10)
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "**The core puzzle:** Account ownership grew only +3pp (2021-2024) while the "
        "Mobile Money Account Rate roughly doubled in the same window. See the "
        "**Trends** page for a channel-by-channel breakdown."
    )

    # =====================================================================
# PAGE 2: TRENDS
# =====================================================================
elif page == "Trends":
    st.title("Trends")
    st.caption("Explore indicator trends and compare digital payment channels.")

    st.subheader("Account Ownership vs. Mobile Money Account Rate")
    min_year, max_year = int(access["observation_date"].dt.year.min()), int(access["observation_date"].dt.year.max())
    year_range = st.slider("Date range", min_year, max_year, (min_year, max_year))

    access_f = access[(access["observation_date"].dt.year >= year_range[0]) & (access["observation_date"].dt.year <= year_range[1])]
    mm_f = usage_proxy[(usage_proxy["observation_date"].dt.year >= year_range[0]) & (usage_proxy["observation_date"].dt.year <= year_range[1])]

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=access_f["observation_date"], y=access_f["value_numeric"], name="Account Ownership (%)",
                               mode="lines+markers", line=dict(color="#2a7f62", width=3), yaxis="y1"))
    fig1.add_trace(go.Scatter(x=mm_f["observation_date"], y=mm_f["value_numeric"], name="Mobile Money Account Rate (%)",
                               mode="lines+markers", line=dict(color="#c94c4c", width=3), yaxis="y2"))
    fig1.update_layout(
        yaxis=dict(title=dict(text="Account Ownership (%)", font=dict(color="#2a7f62"))),
        yaxis2=dict(title=dict(text="Mobile Money Account Rate (%)", font=dict(color="#c94c4c")), overlaying="y", side="right"),
        hovermode="x unified", legend=dict(orientation="h", y=1.1),
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()
    st.subheader("Channel Comparison: Telebirr vs. M-Pesa vs. P2P/ATM Rails")
    channel_options = {
        "Telebirr Registered Users": "USG_TELEBIRR_USERS",
        "M-Pesa Registered Users": "USG_MPESA_USERS",
        "M-Pesa 90-Day Active Users": "USG_MPESA_ACTIVE",
        "P2P Transaction Count": "USG_P2P_COUNT",
        "ATM Transaction Count": "USG_ATM_COUNT",
    }
    selected = st.multiselect("Select channels to compare", list(channel_options.keys()),
                               default=["Telebirr Registered Users", "M-Pesa Registered Users"])

    if selected:
        rows = []
        for label in selected:
            code = channel_options[label]
            vals = obs[obs["indicator_code"] == code]
            for _, r in vals.iterrows():
                rows.append({"Channel": label, "Value": r["value_numeric"], "Date": r["observation_date"]})
        chart_df = pd.DataFrame(rows)
        fig2 = px.bar(chart_df, x="Channel", y="Value", color="Channel", text_auto=".2s",
                      labels={"Value": "Count"})
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Select at least one channel above.")

    st.divider()
    st.subheader("Event Timeline")
    events_sorted = events.dropna(subset=["observation_date"]).sort_values("observation_date")
    fig3 = px.scatter(events_sorted, x="observation_date", y=[1] * len(events_sorted),
                       hover_name="indicator", hover_data={"category": True, "source_name": True},
                       labels={"observation_date": "Date"})
    fig3.update_traces(marker=dict(size=14, color="#c94c4c"))
    fig3.update_yaxes(visible=False)
    fig3.update_layout(showlegend=False, height=250)
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("Hover over a point to see the event name, category, and source.")
    # =====================================================================
# PAGE 3: FORECASTS
# =====================================================================
elif page == "Forecasts":
    st.title("Forecasts")
    st.caption("Access and Usage forecasts, 2025-2027, from Task 4's calibrated event-augmented model.")

    model_choice = st.selectbox(
        "Forecast model",
        ["Scenario range (pessimistic/base/optimistic)", "Base case only"],
    
    )

    acc_scen = access_scenarios(access, links_full)
    access_2024 = access[access["observation_date"].dt.year == 2024]["value_numeric"].iloc[0]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=access["observation_date"].dt.year, y=access["value_numeric"],
                              name="Historical (Findex)", mode="lines+markers",
                              line=dict(color="#2a7f62", width=3)))

    years_f = [2024] + list(acc_scen.index)
    base_f = [access_2024] + acc_scen["base"].tolist()
    fig.add_trace(go.Scatter(x=years_f, y=base_f, name="Base case (event-augmented)",
                              mode="lines+markers", line=dict(color="#3b6fa0", width=3, dash="solid")))

    if model_choice.startswith("Scenario"):
        opt_f = [access_2024] + acc_scen["optimistic"].tolist()
        pes_f = [access_2024] + acc_scen["pessimistic"].tolist()
        fig.add_trace(go.Scatter(x=years_f + years_f[::-1], y=opt_f + pes_f[::-1],
                                  fill="toself", fillcolor="rgba(59,111,160,0.15)",
                                  line=dict(color="rgba(255,255,255,0)"), name="Pessimistic-Optimistic range",
                                  hoverinfo="skip"))

    target_row = targets[targets["indicator_code"] == "ACC_OWNERSHIP"]
    if not target_row.empty:
        nfis_target = target_row["value_numeric"].iloc[0]
        nfis_year = int(float(target_row["fiscal_year"].iloc[0]))
        fig.add_hline(y=nfis_target, line_dash="dot", line_color="#c94c4c",
                      annotation_text=f"NFIS-II target: {nfis_target:.0f}% by {nfis_year}")

    fig.update_layout(title="Access (Account Ownership) Forecast", yaxis_title="Account Ownership (%)",
                       xaxis_title="Year", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    gap = nfis_target - acc_scen.loc[2025, "base"]
    st.error(
        f"**Base-case 2025 forecast ({acc_scen.loc[2025,'base']:.1f}%) is {gap:.1f}pp short "
        f"of the NFIS-II target ({nfis_target:.0f}%).** Even the optimistic scenario "
        f"({acc_scen.loc[2025,'optimistic']:.1f}%) falls well short."
    )

    st.divider()
    st.subheader("Usage Proxy Forecast (Mobile Money Account Rate)")
    st.caption("No indicator directly measures 'digital payment adoption' in this dataset "
               "\u2014 Mobile Money Account Rate is used as the closest available proxy. "
               "Built from only 2 historical points (2021, 2024), so treat as illustrative.")
    usage_2024 = usage_proxy[usage_proxy["observation_date"].dt.year == 2024]["value_numeric"].iloc[0]
    usage_scen = usage_proxy_scenarios(usage_proxy)

    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=usage_proxy["observation_date"].dt.year, y=usage_proxy["value_numeric"],
                               name="Historical (Findex) - proxy", mode="lines+markers",
                               line=dict(color="#c94c4c", width=3)))
    years_u = [2024] + list(usage_scen.index)
    base_u = [usage_2024] + usage_scen["base"].tolist()
    opt_u = [usage_2024] + usage_scen["optimistic"].tolist()
    pes_u = [usage_2024] + usage_scen["pessimistic"].tolist()
    fig4.add_trace(go.Scatter(x=years_u, y=base_u, name="Base case", mode="lines+markers",
                               line=dict(color="#e8a33d", width=3)))
    fig4.add_trace(go.Scatter(x=years_u + years_u[::-1], y=opt_u + pes_u[::-1], fill="toself",
                               fillcolor="rgba(232,163,61,0.15)", line=dict(color="rgba(255,255,255,0)"),
                               name="Pessimistic-Optimistic range", hoverinfo="skip"))
    fig4.update_layout(yaxis_title="Mobile Money Account Rate (%)", xaxis_title="Year", hovermode="x unified")
    st.plotly_chart(fig4, use_container_width=True)

    # =====================================================================
# PAGE 4: INCLUSION PROJECTIONS
# =====================================================================
elif page == "Inclusion Projections":
    st.title("Inclusion Projections")
    st.caption("Progress toward official targets and direct answers to the consortium's questions.")

    scenario_pick = st.select_slider("Scenario", options=["Pessimistic", "Base", "Optimistic"], value="Base")
    scen_key = scenario_pick.lower()

    acc_scen = access_scenarios(access, links_full)
    target_row = targets[targets["indicator_code"] == "ACC_OWNERSHIP"]
    nfis_target = target_row["value_numeric"].iloc[0]
    nfis_year = int(float(target_row["fiscal_year"].iloc[0]))

    forecast_2025 = acc_scen.loc[2025, scen_key]
    progress_pct = min(forecast_2025 / nfis_target, 1.0)

    col1, col2 = st.columns([2, 1])
    with col1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=forecast_2025,
            delta={"reference": nfis_target, "increasing": {"color": "#c94c4c"}, "decreasing": {"color": "#c94c4c"}},
            gauge={"axis": {"range": [0, 100]},
                   "bar": {"color": "#3b6fa0"},
                   "steps": [{"range": [0, nfis_target], "color": "#f2f2f2"}],
                   "threshold": {"line": {"color": "#c94c4c", "width": 4}, "value": nfis_target}},
            title={"text": f"Account Ownership {scenario_pick} Forecast vs. NFIS-II {nfis_year} Target ({nfis_target:.0f}%)"},
        ))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.metric(f"{scenario_pick} 2025 Forecast", f"{forecast_2025:.1f}%")
        st.metric("Gap to Target", f"{nfis_target - forecast_2025:.1f}pp short")
        st.metric("Progress to Target", f"{progress_pct*100:.0f}%")
    st.divider()
    st.subheader("Answering the Consortium's Questions")
    with st.expander("1. What drives financial inclusion in Ethiopia?", expanded=True):
        st.write(
            "Infrastructure enablers (4G coverage, electricity access, smartphone adoption) grew "
            "steadily over 2021-2024 even as Account Ownership growth slowed to +3pp \u2014 suggesting "
            "infrastructure supply is *not* the binding constraint. The barrier is more likely "
            "elsewhere: KYC/ID requirements, trust, or the fact that most new mobile money "
            "accounts are opened by people who already have a bank account (only ~0.5% of "
            "adults are mobile-money-only) rather than reaching genuinely new users."
        )
    with st.expander("2. How do events affect inclusion outcomes?"):
        st.write(
            "Modestly and slowly. Task 3's historical validation found that the cataloged events, "
            "combined at face value, would over-predict observed 2021-2024 Access growth by "
            "roughly 6x \u2014 a 0.153x calibration factor was required to match reality. Calibrated "
            "event effects add only ~1-1.3pp/year to Access, an order of magnitude smaller than "
            "raw comparable-country literature estimates would suggest."
        )
    with st.expander("3. How did inclusion change in 2025, and where is it headed for 2026-2027?"):
        st.write(
            f"Access is forecast to reach roughly 51-55% by 2027 depending on scenario \u2014 "
            f"still well below the NFIS-II target of {nfis_target:.0f}%. The Usage proxy "
            "(mobile money account rate) is forecast to continue growing, roughly 12-17% by 2027, "
            "though with much wider uncertainty given only 2 historical data points."
        )
    st.divider()
    st.subheader("Full Scenario Table")
    st.dataframe(acc_scen.round(1).rename(columns=str.title), use_container_width=True)