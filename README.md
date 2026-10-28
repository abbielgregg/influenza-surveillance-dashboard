# PROJECT IN PROGRESS

# East Midlands Influenza Surveillance Dashboard
This project analyses weekly influenza surveillance data for the East Midlands, sourced from the [UKHSA Data Dashboard API](https://api.ukhsa-dashboard.data.gov.uk/themes/infectious_disease/sub_themes/respiratory/topics/Influenza/geography_types/UKHSA%20Region/geographies/East%20Midlands/metrics?format=api). It pulls hospital admission rates, ICU/HDU admission rates, and test positivity, presenting them as an interactive dashboard to explore trends directly. England-level data from the same API can be overlaid to compare the region with the national picture. It runs on a weekly schedule via GitHub Actions, automatically pulling new data as UKHSA publishes it. 

The project was built to advance my technical skills, following my [RNA-seq reproducibility project](https://github.com/abbielgregg/rna-seq-hpc-pipeline) to move from molecular-level analysis to population-level public health surveillance. Each project has a similar emphasis on transparent, reproducible data handling. I also wanted to develop a project using Python. 

View the live dashboard **[here](https://influenza-surveillance-eastmidlands.streamlit.app)**.

## Data Availability 

Data comes from the UKHSA Data Dashboard API for two geographies: East Midlands (UKHSA Region) and England (Nation). All three metrics are rates per 100,000 population (admissions) or a percentage (positivity), so the two geographies are directly comparable.

**East Midlands**
- Test positivity: 2017 to present, reported year-round.
- Hospital admission rate and ICU/HDU admission rate: 2020 to present. UKHSA reports these seasonally, during the winter flu season, so both series have gaps over summer.
- The "complete overlap" dataset (weeks where all three metrics have data) covers 2020-09-28 onwards.

**England**
- Hospital admission rate and ICU/HDU admission rate: 2015 to present.
- Test positivity: 2017 to present.

### Cleaning the Data

- **Age bands:** The England files also contain rows for individual age groups. I kept only the all-ages, all-sexes rows (`age == "all"`, `sex == "all"`) so there is one row per week.
- **Duplicate week:** The week of 2018-01-01 appeared twice in the England ICU/HDU dataset, with UKHSA publishing two different values for that same week (0.40 and 0.51). I resolved this by keeping the last published value, assuming it was an updated figure. The cleaning script prints a warning when this happens.

## Outlier Detection
Standard IQR-based potential outlier detection flagged a notable number of points across all three metrics: 16 for hospital admissions, 43 for ICU/HDU admissions, and 58 for test positivity. 

Visual inspection of the time series confirms these are not data quality issues. They correspond to expected winter flu season peaks, which recur predictably every year. IQR methods assume a roughly stable distribution and are not well suited to inherently seasonal data like this. 

A seasonally-aware method e.g. comparing each point to the same calendar week in other years would be more appropriate for genuine anomaly detection in this dataset.

Cross-referencing with [UKHSA's Winter 2022 to 2023 seasonal respiratory surveillance report](https://www.gov.uk/government/statistics/influenza-in-the-uk-annual-epidemiological-reports/surveillance-of-influenza-and-other-seasonal-respiratory-viruses-in-the-uk-winter-2022-to-2023) confirms the largest spike in this dataset (hospital admissions and ICU/HDU admissions both peaking around week 51 2022) matches a nationally-documented, unusually severe flu season, not a data anomaly.

## Progress
- [x] Explored UKHSA API and confirmed East Midlands influenza data availability
- [x] Selected three metrics: hospital admissions, ICU/HDU admissions, test positivity
- [x] Built fetch script to pull and save raw data via the API
- [x] Clean and merge datasets (align weekly dates across all three metrics)
- [x] Exploratory analysis — check for seasonality (average across all years), missing data, outliers
- [x] Build first dashboard (Streamlit)
- [x] CI/CD GitHub actions: Update with future UKHSA published data
- [x] Deploy first dashboard
- [x] Add a public health analysis section in docs
- [x] Add a section to download the .csv files
- [x] Make sidebar tags the same colour as lines on the graph
- [x] Fetch and clean England data, with a toggle to compare it against East Midlands
- [x] Dynamic chart title based on the selected metrics
- [ ] Add a ML aspect 
- [ ] Add a storyboard/slideshow of key findings (e.g. incl 2022-2023 flu surge)
- [ ] Add to the public health analysis section in docs
- [ ] Expand dataset to show population density (map) for East Mids
- [ ] Same as above for whole nation data
- [ ] Stats test: is this seasons peak statistically higher than the historical average?
- [ ] Architecture diagram to show the pipeline of repo (add to README)
- [ ] A short demo vid/gif showing the dashboard in action (add to README)