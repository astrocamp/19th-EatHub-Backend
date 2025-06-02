import csv
import os
import sys
import time

import django

from restaurants.models import Restaurant
from utilities.place_api import nearby_search

# 這邊是初始化django 是為了讓這支檔案可以使用django的ORM
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

CSV_PATH = "utilities/data_builder/grid_points.csv"
SEARCH_RADIUS = 720


def main():
    hotspots = []

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader, start=1):
            location = f"{row['Y']},{row['X']}"
            print(f"({i}) 正在查詢 {location}")
            results = nearby_search(location, SEARCH_RADIUS)

            if len(results) >= 60:
                hotspots.append([location, SEARCH_RADIUS])

            for place in results:
                Restaurant.objects.update_or_create(
                    place_id=place["place_id"], defaults=place
                )

            time.sleep(1)
        if hotspots:
            with open("hotspots.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["location", "radius"])
                writer.writerows(hotspots)


if __name__ == "__main__":
    main()
