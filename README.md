# PROJECT IN PROGRESS

# East Midlands Influenza Surveillance Dashboard
This project analyses weekly influenza surveillance data for the East Midlands, sourced from the [UKHSA Data Dashboard API](https://api.ukhsa-dashboard.data.gov.uk/themes/infectious_disease/sub_themes/respiratory/topics/Influenza/geography_types/UKHSA%20Region/geographies/East%20Midlands/metrics?format=api). It pulls hospital admission rates, ICU/HCU admission rates, and test positivity, presenting them as an interactive dashboard to explore trends directly. 

The project was built to advance my technical skills, following my [RNA-seq reproducibility project](https://github.com/abbielgregg/rna-seq-hpc-pipeline) to move from molecular-level analysis to population-level public health surveillance. Each project has a similar emphasis on transparent, reproducible data handling. This pipeline runs on a weekly schedule via GitHub Actions, automatically pulling new data as UKHSA publishes it. 

View the live dashboard **[here](https://influenza-surveillance-eastmidlands.streamlit.app)**.

## Data Availability 
- Test positivity: complete coverage, 2017–present (reported year-round, weekly in season / fortnightly in summer)
- ICU/HDU admission rate: available 2020–present, but currently paused. UKHSA confirms seasonal reporting: the 2025–2026 FluSurvey season ended 16 April 2026, and hospitalisation-related metrics pause over summer, resuming for winter 2026 ([UKHSA source](https://ukhsa-dashboard.data.gov.uk/respiratory-viruses/influenza)).
- Hospital admission rate: available 2020-09-28 to 2024-05-13 under the "East Midlands" (UKHSA Region) geography. This predates UKHSA's regional geography restructuring (9 UKHSA Regions → 4 UKHSA Super Regions, effective 30 September 2024), which changed how this metric is reported at the East Midlands level going forward.

The combined "complete overlap" dataset is limited to the hospital admission rate's availability window (up to 2024-05-13). Test positivity continues year-round and is shown separately on the live dashboard.

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
- [x] Exploratory analysis — check for seasonality (average across all years), missing data, outliers
- [x] Build first dashboard (Streamlit)
- [x] Deploy first dashboard
- [x] Write up findings / add public health context section
- [ ] Make graphs for seasonality by year
- [ ] Add ideas from notion to dashboard

