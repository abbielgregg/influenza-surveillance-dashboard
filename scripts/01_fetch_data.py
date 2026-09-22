import requests
import pandas as pd

# Data collected from UKHSA API URLs, requests up to 365 records per page

BASE = "https://api.ukhsa-dashboard.data.gov.uk/themes/infectious_disease/sub_themes/respiratory/topics/Influenza/geography_types/UKHSA%20Region/geographies/East%20Midlands/metrics/"

metrics = [
    "influenza_healthcare_hospitalAdmissionRateByWeek",
    "influenza_healthcare_ICUHDUadmissionRateByWeek",
    "influenza_testing_positivityByWeek"
]

for metric in metrics:
    url = f"{BASE}{metric}?page_size=365"
    all_results = []
    while url:
        response = requests.get(url)
        data = response.json()
        all_results.extend(data["results"])
        url = data["next"] # Follows the "next" link automatically to get the full dataset

    df = pd.DataFrame(all_results)
    df.to_csv(f"data/raw/{metric}.csv", index=False)
    print(f"Saved {len(df)} rows for {metric}")