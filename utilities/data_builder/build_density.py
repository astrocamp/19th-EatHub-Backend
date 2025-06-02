import math

import pandas as pd


def calc_radius_m(density, safe_factor=0.25, limit=60):
    if density == 0:
        return 5000
    area_needed = (limit / density) * safe_factor
    radius_km = math.sqrt(area_needed / math.pi)
    radius_m = math.ceil(radius_km * 1000 / 100) * 100
    return max(min(radius_m, 5000), 500)


df_restaurants = pd.read_csv("utilities/data_builder/registered_restaurants.csv")
df_area = pd.read_csv("utilities/data_builder/district_area_cleaned_full.csv")

results = []
for _, row in df_area.iterrows():
    county = row["county"]
    district = row["district"]
    area = row["area"]
    keyword = f"{county}{district}"

    mask = df_restaurants["公司地址"].astype(str).str.contains(keyword)
    count = mask.sum()

    results.append(
        {
            "county": county,
            "district": district,
            "area": area,
            "restaurant_count": count,
            "join_key": county + district,
        }
    )

df_density = pd.DataFrame(results)
df_density["density"] = round(df_density["restaurant_count"] / df_density["area"], 2)
df_density["suggested_radius_m"] = df_density["density"].apply(calc_radius_m)
df_density.to_csv(
    "utilities/data_builder/restaurant_density.csv", index=False, encoding="utf-8-sig"
)
