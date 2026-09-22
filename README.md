# Influenza Surveillance Dashboard Project
Analysis of UKHSA influenza surveillance data for the East Midlands, looking at test positivity, hospital admissions, and ICU/HDU admissions.

## Data Availability Notes
- Test positivity: complete coverage, 2017 - present
- ICU/HDU admission rate: complete coverage, 2020 - present
- Hospital admission rate: only available 2020-09-28 to 2024-05-13 (reporting appears to have stopped after this date)

The combined "complete overlap" dataset is limited to the hospital admission rate's timeframe (up to 2024-05-13). Test positivity and ICU/HDU admission data continue beyond this and could be explored separately in future work. 

## Progress
- [x] Explored UKHSA API and confirmed East Midlands influenza data availability
- [x] Selected three metrics: hospital admissions, ICU/HDU admissions, test positivity
- [x] Built fetch script to pull and save raw data via the API
- [x] Clean and merge datasets (align weekly dates across all three metrics)
- [ ] Exploratory analysis — check for seasonality, missing data, outliers
- [ ] Build dashboard (Streamlit)
- [ ] Deploy dashboard
- [ ] Write up findings / add public health context section

