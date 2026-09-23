import streamlit as st
import pandas as pd

st.set_page_config(page_title="East Midlands Flu Surveillance", layout="wide")

st.title("East Midlands Influenza Surveillance Dashboard")
st.write("Weekly influenza metrics for the East Midlands region, sourced from UKHSA.")
st.info(
    "**Data note:** Hospital admission rate data is only available up to 2024-05-13. "
    "UKHSA restructured regional reporting geographies (9 UKHSA Regions → 4 UKHSA Super Regions) "
    "from 30 September 2024, which affected how this metric is reported at the East Midlands level. "
    "Test positivity and ICU/HDU admission rate continue to be reported and are shown beyond this date."
)

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

# Mapping between display names and actual column names
metric_labels = {
    "Hospital Admission Rate": "hospital_admission_rate",
    "ICU/HDU Admission Rate": "icu_hdu_admission_rate",
    "Test Positivity": "test_positivity"
}

selected_labels = st.sidebar.multiselect(
    "Select metrics to display",
    options=list(metric_labels.keys()),
    default=list(metric_labels.keys())
)

# Convert the selected labels back to actual column names
metrics = [metric_labels[label] for label in selected_labels]

# Filter data based on selections 
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)]
else:
    filtered = df

# Display 
if metrics:
    display_df = filtered.set_index("date")[metrics].rename(columns={v: k for k, v in metric_labels.items()})
    st.line_chart(display_df)
else:
    st.warning("Select at least one metric to display.")

st.caption(f"Showing {len(filtered)} weeks of data.")