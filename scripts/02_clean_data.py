import pandas as pd

metric_files = {
    "hospital_admission_rate": "influenza_healthcare_hospitalAdmissionRateByWeek",
    "icu_hdu_admission_rate": "influenza_healthcare_ICUHDUadmissionRateByWeek",
    "test_positivity": "influenza_testing_positivityByWeek",
}

for prefix in ["east_midlands", "england"]:
    dfs = []
    for column_name, metric in metric_files.items():
        filepath = f"data/raw/{prefix}_{metric}.csv"
        df = pd.read_csv(filepath)
        assert "date" in df.columns and "metric_value" in df.columns, f"Missing expected columns in {filepath}"

        # Keep only the all-ages, all-sexes rows (one row per week)
        df = df[(df["age"] == "all") & (df["sex"] == "all")]
        assert len(df) > 0, f"No rows left after filtering in {filepath}"

        # UKHSA published two values for the same week so I kept the last value (0.51)
        n_dups = df["date"].duplicated().sum()
        if n_dups > 0:
            print(f"Warning: {n_dups} duplicate date(s) in {filepath}, keeping the last value")
            df = df.drop_duplicates(subset="date", keep="last")

        assert df["date"].is_unique, f"Duplicate dates in {filepath}, check the filter"

        df = df[["date", "metric_value"]].rename(columns={"metric_value": column_name})
        df["date"] = pd.to_datetime(df["date"])
        dfs.append(df)

    merged = dfs[0]
    for df in dfs[1:]:
        merged = merged.merge(df, on="date", how="outer")

    merged = merged.sort_values("date").reset_index(drop=True)
    merged.to_csv(f"data/processed/{prefix}_flu_merged.csv", index=False)
    print(f"{prefix}: {len(merged)} rows, from {merged['date'].min()} to {merged['date'].max()}")
    print(merged.isna().sum())

    # Trim to the range where all three metrics have data
    merged_complete = merged.dropna()
    merged_complete.to_csv(f"data/processed/{prefix}_flu_merged_complete.csv", index=False)
    print(f"{prefix} complete overlap: {len(merged_complete)} rows, from {merged_complete['date'].min()} to {merged_complete['date'].max()}")