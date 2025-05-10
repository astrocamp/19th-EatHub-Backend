import requests
import time
from dotenv import load_dotenv
import os

GOOGLE_MAP_API_BASE_URL = 'https://maps.googleapis.com/maps/api/place'

def text_search(keyword, location, radius, count=61):
    load_dotenv()
    API_KEY = os.getenv('GOOGLE_API_KEY')
    query = keyword
    language = 'zh-TW'
    url = f'{GOOGLE_MAP_API_BASE_URL}/textsearch/json?query={query}&location={location}&radius={radius}&language={language}&key={API_KEY}'

    result = []

    while True:
        response = requests.get(url)
        data = response.json()

        if data.get('status') != 'OK':
            break
        
        for place in data.get('results', []):
            result.append({
            'name': place.get('name'),
            'address': place.get('formatted_address'),
            'rating': place.get('rating'),
            'latitude': place['geometry']['location']['lat'],
            'longitude': place['geometry']['location']['lng'],
            'types': place.get('types', []),
            'placeId': place.get('place_id'),
            })

            if len(result) >= count:
                return result

        next_page_token = data.get('next_page_token')

        if next_page_token:
            time.sleep(3)
            url = f'{GOOGLE_MAP_API_BASE_URL}/textsearch/json?pagetoken={next_page_token}&key={API_KEY}'
        else:
            break

    return result