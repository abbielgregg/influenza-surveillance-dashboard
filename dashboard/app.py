import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="East Midlands Flu Surveillance", layout="wide")

st.markdown("""
<style>
span[aria-label="Hospital Admission Rate"] {
    background-color: #0068C9 !important;
    border-color: #0068C9 !important;
}
span[aria-label="ICU/HDU Admission Rate"] {
    background-color: #83C9FF !important;
    border-color: #83C9FF !important;
    color: #0E1117 !important;
}
span[aria-label="Test Positivity"] {
    background-color: #FF2B2B !important;
    border-color: #FF2B2B !important;
}
</style>
""", unsafe_allow_html=True)

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

df = pd.read_csv("data/processed/east_midlands_flu_merged.csv", parse_dates=["date"])
df_england = pd.read_csv("data/processed/england_flu_merged.csv", parse_dates=["date"])

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

# Mapping between display names and their fixed chart colours
metric_colors = {
    "Hospital Admission Rate": "#0068C9",
    "ICU/HDU Admission Rate": "#83C9FF",
    "Test Positivity": "#FF2B2B"
}

selected_labels = st.sidebar.multiselect(
    "Select metrics to display",
    options=list(metric_labels.keys()),
    default=list(metric_labels.keys())
)

compare_england = st.sidebar.checkbox("Compare with England", value=False)

# Convert the selected labels back to actual column names
metrics = [metric_labels[label] for label in selected_labels]

# Filter data based on selections
filtered = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)]
filtered_england = df_england[(df_england["date"].dt.date >= start_date) & (df_england["date"].dt.date <= end_date)]


def to_long(data, region):
    """Reshape to one row per date/metric/region, which Altair needs."""
    out = data[["date"] + metrics].rename(columns={v: k for k, v in metric_labels.items()})
    out = out.melt(id_vars="date", var_name="Metric", value_name="Value")
    out["Region"] = region
    return out


# Display
if metrics:
    display_df = filtered.set_index("date")[metrics].rename(columns={v: k for k, v in metric_labels.items()})
    display_df.index = display_df.index.date  # strips the time component, keeps just the date
    display_df.index.name = "Date"

    tab1, tab2, tab3 = st.tabs(["Chart", "Tabular data", "Download"])

    with tab1:
        # Dynamic title and y-axis label 
        if len(selected_labels) == len(metric_labels):
            metric_part = "All metrics"
        elif len(selected_labels) == 2:
            metric_part = " and ".join(selected_labels)
        else:
            metric_part = selected_labels[0]

        region_part = "East Midlands vs England" if compare_england else "East Midlands"
        chart_title = f"{metric_part}: {region_part}"

        if selected_labels == ["Test Positivity"]:
            y_title = "Test positivity (%)"
        elif "Test Positivity" not in selected_labels:
            y_title = "Admissions per 100,000"
        else:
            y_title = "Rate per 100,000 (admissions) / % (positivity)"

        # Data 
        long_df = to_long(filtered, "East Midlands")
        if compare_england:
            long_df = pd.concat([long_df, to_long(filtered_england, "England")])

        # Chart
        chart = alt.Chart(long_df).mark_line().encode(
            x=alt.X("date:T", title=None),
            y=alt.Y("Value:Q", title=y_title, scale=alt.Scale(domainMin=0)),
            color=alt.Color(
                "Metric:N",
                scale=alt.Scale(
                    domain=selected_labels,
                    range=[metric_colors[label] for label in selected_labels],
                ),
            ),
            strokeDash=alt.StrokeDash(
                "Region:N",
                scale=alt.Scale(
                    domain=["East Midlands", "England"],
                    range=[[1, 0], [5, 3]],
                ),
            ),
            tooltip=["date:T", "Metric:N", "Region:N", "Value:Q"],
        ).properties(title=chart_title)
        st.altair_chart(chart, width="stretch")

    with tab2:
        st.dataframe(display_df, width="stretch")

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