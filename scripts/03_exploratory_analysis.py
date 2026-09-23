import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/flu_merged.csv", parse_dates=["date"])

# --- 1. Missing data check ---
print("=== Missing Data ===")
print(df.isna().sum())
print()

# Basic summary stats (helps spot outliers)
print("=== Summary Statistics ===")
print(df.describe())
print()

# Simple outlier flagging using IQR 
print("=== Potential Outliers (IQR method) ===")
for col in ["hospital_admission_rate", "icu_hdu_admission_rate", "test_positivity"]:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    print(f"{col}: {len(outliers)} potential outliers (bounds: {lower:.2f} to {upper:.2f})")

print()

# Visual check: time series for each metric 
fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

axes[0].plot(df["date"], df["hospital_admission_rate"], color="steelblue")
axes[0].set_title("Hospital Admission Rate")

axes[1].plot(df["date"], df["icu_hdu_admission_rate"], color="darkorange")
axes[1].set_title("ICU/HDU Admission Rate")

axes[2].plot(df["date"], df["test_positivity"], color="seagreen")
axes[2].set_title("Test Positivity (%)")

plt.tight_layout()
plt.savefig("data/processed/exploratory_timeseries.png")
print("Saved time series plot to data/processed/exploratory_timeseries.png")

# Seasonality check: average by month across all years (fixed scaling)
df["month"] = df["date"].dt.month
monthly_avg = df.groupby("month")[["hospital_admission_rate", "icu_hdu_admission_rate", "test_positivity"]].mean()

fig2, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(monthly_avg.index, monthly_avg["hospital_admission_rate"], marker="o", color="steelblue", label="Hospital Admission Rate")
ax1.plot(monthly_avg.index, monthly_avg["test_positivity"], marker="o", color="seagreen", label="Test Positivity (%)")
ax1.set_xlabel("Month")
ax1.set_ylabel("Hospital Admission Rate / Test Positivity")
ax1.set_xticks(range(1, 13))

ax2 = ax1.twinx()
ax2.plot(monthly_avg.index, monthly_avg["icu_hdu_admission_rate"], marker="o", color="darkorange", label="ICU/HDU Admission Rate")
ax2.set_ylabel("ICU/HDU Admission Rate")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.title("Average Metric Value by Month (Seasonality Check)")
plt.tight_layout()
plt.savefig("data/processed/exploratory_seasonality.png")
print("Saved seasonality plot to data/processed/exploratory_seasonality.png")