# Influenza Surveillance Dashboard Project
Analysis of UKHSA influenza surveillance data for the East Midlands, looking at test positivity, hospital admissions, and ICU/HDU admissions.

## Data Availability 
- Test positivity: complete coverage, 2017 - present
- ICU/HDU admission rate: complete coverage, 2020 - present
- Hospital admission rate: only available 2020-09-28 to 2024-05-13 (reporting appears to have stopped after this date)

The combined "complete overlap" dataset is limited to the hospital admission rate's timeframe (up to 2024-05-13). Test positivity and ICU/HDU admission data continue beyond this and could be explored separately in future work. 

## Outlier Detection
Standard IQR-based potential outlier detection flagged a notable number of points across all three metrics: 16 for hospital admissions, 43 for ICU/HCU admissions, and 58 for test positivity. 

Visual inspection of the time series confirms these are not data quality issues. They correspond to expected winter flu season peaks, which recur predictably every year. IQR methods assume a roughly stable distribution and are not well suited to inherently seasonal data like this. 

A seasonally-aware method e.g. comparing each point to the same calendar week in other years would be more appropriate for genuine anomaly detection in this dataset 

Cross-referencing with [UKHSA's Winter 2022 to 2023 seasonal respiratory surveillance report](https://www.gov.uk/government/statistics/surveillance-of-influenza-and-other-seasonal-respiratory-viruses-in-the-uk-winter-2022-to-2023) confirms the largest spike in this dataset (hospital admissions and ICU/HDU admissions both peaking around week 51 2022) matches a nationally-documented, unusually severe flu season, not a data anomaly.

## Progress
- [x] Explored UKHSA API and confirmed East Midlands influenza data availability
- [x] Selected three metrics: hospital admissions, ICU/HDU admissions, test positivity
- [x] Built fetch script to pull and save raw data via the API
- [x] Clean and merge datasets (align weekly dates across all three metrics)
- [ ] Exploratory analysis — check for seasonality, missing data, outliers
- [ ] Build dashboard (Streamlit)
- [ ] Deploy dashboard
- [ ] Write up findings / add public health context section

