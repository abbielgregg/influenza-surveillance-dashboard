import pandas as pd

files = {
    "hospital_admission_rate": "data/raw/influenza_healthcare_hospitalAdmissionRateByWeek.csv",
    "icu_hdu_admission_rate": "data/raw/influenza_healthcare_ICUHDUadmissionRateByWeek.csv",
    "test_positivity": "data/raw/influenza_testing_positivityByWeek.csv"
}

dfs = []
for column_name, filepath in files.items():
    df = pd.read_csv(filepath)
    assert "date" in df.columns and "metric_value" in df.columns, f"Missing expected columns in {filepath}"
    df = df[["date", "metric_value"]].rename(columns={"metric_value": column_name})
    df["date"] = pd.to_datetime(df["date"])
    dfs.append(df)

merged = dfs[0]
for df in dfs[1:]:
    merged = merged.merge(df, on="date", how="outer")

merged = merged.sort_values("date").reset_index(drop=True)

merged.to_csv("data/processed/flu_merged.csv", index=False)
print(f"Merged dataset: {len(merged)} rows, from {merged['date'].min()} to {merged['date'].max()}")
print(merged.isna().sum())

# Trim to the range where all three metrics have data

merged_complete = merged.dropna()
merged_complete.to_csv("data/processed/flu_merged_complete.csv", index=False)
print(f"Complete-overlap dataset: {len(merged_complete)} rows, from {merged_complete['date'].min()} to {merged_complete['date'].max()}")

