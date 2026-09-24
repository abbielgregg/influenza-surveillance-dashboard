import streamlit as st
import pandas as pd

st.set_page_config(page_title="East Midlands Flu Surveillance", layout="wide")

st.title("East Midlands Influenza Surveillance Dashboard")
st.write("Weekly influenza metrics for the East Midlands region, sourced from UKHSA.")
st.info(
    "**Data note:** UKHSA pauses hospitalisation-related flu metrics over summer — "
    "the 2025–2026 season ended 16 April 2026, with ICU/HDU and hospital admission data "
    "resuming for winter 2026. Hospital admission rate is additionally affected by UKHSA's "
    "September 2024 regional geography restructuring (9 Regions → 4 Super Regions), which "
    "changed how it's reported at the East Midlands level from that point on. Test positivity "
    "is reported year-round and is shown up to the most recent available week."
)

df = pd.read_csv("data/processed/flu_merged.csv", parse_dates=["date"])

# --- Sidebar controls ---
st.sidebar.header("Filters")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

# Quick range presets
range_option = st.sidebar.radio(
    "Time range",
    options=[
        "Past Month",
        "Past 3 Months",
        "Past 6 Months",
        "Past Year",
        "Past 2 Years",
        "Last 5 Years",
        "Full History",
        "Custom"
    ],
    index=5  # defaults to "Last 5 Years"
)

preset_offsets = {
    "Past Month": pd.DateOffset(months=1),
    "Past 3 Months": pd.DateOffset(months=3),
    "Past 6 Months": pd.DateOffset(months=6),
    "Past Year": pd.DateOffset(years=1),
    "Past 2 Years": pd.DateOffset(years=2),
    "Last 5 Years": pd.DateOffset(years=5),
}

if range_option in preset_offsets:
    start_date = (pd.Timestamp(max_date) - preset_offsets[range_option]).date()
    end_date = max_date
    st.sidebar.caption(f"{start_date} to {end_date}")
elif range_option == "Full History":
    start_date = min_date
    end_date = max_date
    st.sidebar.caption(f"{start_date} to {end_date}")
else:  # Custom
    date_range = st.sidebar.date_input(
        "Select date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

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
filtered = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)]

# Display
if metrics:
    display_df = filtered.set_index("date")[metrics].rename(columns={v: k for k, v in metric_labels.items()})

    tab1, tab2, tab3 = st.tabs(["Chart", "Tabular data", "Download"])

    with tab1:
        st.line_chart(display_df)

    with tab2:
        st.dataframe(display_df, use_container_width=True)

    with tab3:
    st.write("Download the currently filtered view:")
    filtered_csv = display_df.to_csv().encode("utf-8")
    st.download_button(
        label="Download filtered data as CSV",
        data=filtered_csv,
        file_name="flu_surveillance_filtered.csv",
        mime="text/csv"
    )

    st.write("Or download the full dataset (all dates, all metrics):")
    full_csv = df.rename(columns={v: k for k, v in metric_labels.items()}).to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download full dataset as CSV",
        data=full_csv,
        file_name="flu_surveillance_full.csv",
        mime="text/csv"
    )
else:
    st.warning("Select at least one metric to display.")

st.caption(f"Showing {len(filtered)} weeks of data.")