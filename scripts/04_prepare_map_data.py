import pandas as pd

lookup = pd.read_csv("data/raw/map/Local_Authority_District_to_Region_(April_2025)_Lookup_in_EN_v2.csv")
density = pd.read_csv("data/raw/map /TS006-2021-4-filtered-2026-10-28T12-10-22Z.csv")

# Keep only East Midlands authorities
em = lookup[lookup["RGN25NM"] == "East Midlands"]

# Attach density by matching on the area code
merged = em.merge(
    density,
    left_on="LAD25CD",
    right_on="Lower tier local authorities Code",
    how="left",
)
merged = merged.rename(columns={"Observation": "density_per_km2"})
merged = merged[["LAD25CD", "LAD25NM", "density_per_km2"]]

assert len(merged) == 35, f"Expected 35 East Midlands authorities, got {len(merged)}"
assert merged["density_per_km2"].notna().all(), "Some authorities have no density value"

print(merged.sort_values("density_per_km2"))