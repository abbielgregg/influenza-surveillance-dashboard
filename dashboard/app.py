import streamlit as st
import pandas as pd

st.set_page_config(page_title="East Midlands Flu Surveillance", layout="wide")

st.title("East Midlands Influenza Surveillance Dashboard")
st.write("Weekly influenza metrics for the East Midlands region, sourced from UKHSA.")

df = pd.read_csv("data/processed/flu_merged.csv", parse_dates=["date"])

# Sidebar controls 
st.sidebar.header("Filters")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

metrics = st.sidebar.multiselect(
    "Select metrics to display",
    options=["hospital_admission_rate", "icu_hdu_admission_rate", "test_positivity"],
    default=["hospital_admission_rate", "icu_hdu_admission_rate", "test_positivity"]
)

# Filter data based on selections
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)]
else:
    filtered = df

# Display 
if metrics:
    st.line_chart(filtered.set_index("date")[metrics])
else:
    st.warning("Select at least one metric to display.")

st.caption(f"Showing {len(filtered)} weeks of data.")