import os
import time

import requests
from dotenv import load_dotenv

GOOGLE_MAP_API_BASE_URL = "https://maps.googleapis.com/maps/api/place"
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")


def parse_google_place(place):
    return {
        "name": place.get("name"),
        "address": place.get("formatted_address") or place.get("vicinity"),
        "google_rating": place.get("rating"),
        "latitude": place["geometry"]["location"]["lat"],
        "longitude": place["geometry"]["location"]["lng"],
        "types": ",".join(place.get("types", [])),
        "place_id": place.get("place_id"),
        "user_ratings_total": place.get("user_ratings_total"),
        "google_photo_reference": (
            place.get("photos", [{}])[0].get("photo_reference")
            if place.get("photos")
            else None
        ),
    }


def text_search(keyword, location, radius, count=61):
    url = f"{GOOGLE_MAP_API_BASE_URL}/textsearch/json"
    params = {
        "query": keyword,
        "location": location,
        "radius": radius,
        "language": "zh-TW",
        "key": API_KEY,
    }
    result = []

    while True:
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("status") != "OK":
            break
        for place in data.get("results", []):
            result.append(parse_google_place(place))
            if len(result) >= count:
                return result

        next_page_token = data.get("next_page_token")

        if next_page_token:
            time.sleep(3)
            params = {"pagetoken": next_page_token, "key": API_KEY}
        else:
            break

    return result


def get_google_photo(photo_reference, max_width=400):
    url = (
        f"{GOOGLE_MAP_API_BASE_URL}/photo"
        f"?maxwidth={max_width}&photo_reference={photo_reference}&key={API_KEY}"
    )

    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    return None


def nearby_search(location, radius):
    url = f"{GOOGLE_MAP_API_BASE_URL}/nearbysearch/json"
    params = {
        "location": location,
        "radius": radius,
        "type": "restaurant",
        "language": "zh-TW",
        "key": API_KEY,
    }
    results = []

    while True:
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("status") != "OK":
            break
        for place in data.get("results", []):
            results.append(parse_google_place(place))

        next_page_token = data.get("next_page_token")

        if next_page_token:
            time.sleep(3)
            url = f"{GOOGLE_MAP_API_BASE_URL}/nearbysearch/json"
            params = {"pagetoken": next_page_token, "key": API_KEY}
        else:
            break

    return results


def get_place_details(place_id):
    url = f"{GOOGLE_MAP_API_BASE_URL}/details/json"
    params = {
        "place_id": place_id,
        "fields": "formatted_phone_number,opening_hours",
        "language": "zh-TW",
        "key": API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()
    WEEKDAYS_EN = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]

    if data.get("status") == "OK":
        result = data["result"]
        weekday_text = result.get("opening_hours", {}).get("weekday_text")
        opening_hours = (
            {
                WEEKDAYS_EN[i]: text.split(":", 1)[1].strip()
                for i, text in enumerate(weekday_text)
            }
            if weekday_text
            else {}
        )
        return {
            "place_id": place_id,
            "phone": result.get("formatted_phone_number"),
            "opening_hours": opening_hours,
        }
    else:
        return {"error": data.get("status"), "message": data.get("error_message", "")}
