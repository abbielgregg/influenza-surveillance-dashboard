import requests
import pandas as pd
from urllib.parse import quote

# Data collected from UKHSA API URLs, requests up to 365 records per page

BASE = "https://api.ukhsa-dashboard.data.gov.uk/themes/infectious_disease/sub_themes/respiratory/topics/Influenza/geography_types/{geo_type}/geographies/{geo}/metrics/"

# prefix is used in the filenames so the places don't overwrite each other
places = {
    "east_midlands": ("UKHSA Region", "East Midlands"),
    "england": ("Nation", "England"),
}

metrics = [
    "influenza_healthcare_hospitalAdmissionRateByWeek",
    "influenza_healthcare_ICUHDUadmissionRateByWeek",
    "influenza_testing_positivityByWeek",
]

for prefix, (geo_type, geo) in places.items():
    base = BASE.format(geo_type=quote(geo_type), geo=quote(geo))
    for metric in metrics:
        url = f"{base}{metric}?page_size=365"
        all_results = []
        while url:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            all_results.extend(data["results"])
            url = data["next"]

        df = pd.DataFrame(all_results)
        df.to_csv(f"data/raw/{prefix}_{metric}.csv", index=False)
        print(f"Saved {len(df)} rows for {prefix} / {metric}")