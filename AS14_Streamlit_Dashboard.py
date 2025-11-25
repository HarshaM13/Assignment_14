
# app.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="COVID Deaths Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Data loader (cached)
# -----------------------------
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Optional: ensure Date is parsed properly if needed
    # If Date is in "YYYY-MM-DD" format uncomment below:
    # df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data("data/processed/df_covid_val_pred.csv")

# -----------------------------
# UI - Title & month selector
# -----------------------------
st.title("COVID Deaths Dashboard")

# Put filter in the sidebar (you can move it to main if preferred)
months = list(df['month'].unique())
selected_month = st.sidebar.selectbox("Select month", options=months, index=0)

# Filtered data
filtered_df = df[df['month'] == selected_month]

# -----------------------------
# KPI Card (Total Deaths)
# -----------------------------
total_deaths = int(filtered_df["Deaths"].sum())

# Using Plotly Indicator (visual KPI)
kpi_fig = go.Figure(go.Indicator(
    mode="number",
    value=total_deaths,
    title={"text": f"Total Deaths in {selected_month}"},
    number={"valueformat": ",", "font": {"size": 48}}
))
kpi_fig.update_layout(height=200, margin=dict(t=30, b=0, l=0, r=0))

# You could also use st.metric if you prefer a native Streamlit KPI:
# st.metric(label=f"Total Deaths in {selected_month}", value=f"{total_deaths:,}")

st.plotly_chart(kpi_fig, use_container_width=True)

# -----------------------------
# Charts
# -----------------------------
# Graph 1: Bar chart of Deaths by Date
fig1 = px.bar(
    filtered_df,
    x="Date",
    y="Deaths",
    title=f"Deaths in {selected_month}",
    text="Deaths"
)
fig1.update_traces(textposition="outside")
fig1.update_layout(margin=dict(t=60, b=10, l=10, r=10))

# Graph 2: Bar chart of Predicted Deaths by Date
fig2 = px.bar(
    filtered_df,
    x="Date",
    y="Predicted_Deaths",
    title=f"Predicted Deaths in {selected_month}",
    text="Predicted_Deaths"
)
fig2.update_traces(textposition="outside")
fig2.update_layout(margin=dict(t=60, b=10, l=10, r=10))

# Graph 4: Line chart for overall trend
fig4 = px.line(
    df,
    x="Date",
    y=["Deaths", "Predicted_Deaths"],
    title="Overall Trend of Deaths and Predictions"
)
fig4.update_layout(margin=dict(t=60, b=10, l=10, r=10))

# -----------------------------
# Layout using columns (2x grid)
# -----------------------------
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)  # You can move this to col2 if you prefer
with col2:
    st.plotly_chart(fig2, use_container_width=True)
