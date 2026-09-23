import streamlit as st
import pandas as pd

st.set_page_config(page_title="East Midlands Flu Surveillance", layout="wide")

st.title("East Midlands Influenza Surveillance Dashboard")
st.write("Weekly influenza metrics for the East Midlands region, sourced from UKHSA.")

df = pd.read_csv("data/processed/flu_merged.csv", parse_dates=["date"])

st.line_chart(df.set_index("date")[["hospital_admission_rate", "icu_hdu_admission_rate", "test_positivity"]])