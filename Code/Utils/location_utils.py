import pandas as pd
import geopandas as gpd
import geopy
import urllib.request
import urllib.parse
import json

class location_utils():

    API_KEY = "AhbvYTADoexgk9EW4R5SyOu92avR1sTw"
    POI_CATEGORIES = None

    def get_location(address):
        url = f'https://api.tomtom.com/search/2/geocode/{urllib.parse.quote(address)}.json?key={location_utils.API_KEY}'
        req = urllib.request.urlopen(url)
        data = req.read().decode('utf-8')
        data = json.loads(data)
        return data['results'][0]['position']['lat'], data['results'][0]['position']['lon']

    def get_POI_categories():
        if location_utils.POI_CATEGORIES:
            return location_utils.POI_CATEGORIES
        url = f"https://api.tomtom.com/search/2//poiCategories.json?key={location_utils.API_KEY}"
        req = urllib.request.urlopen(url)
        data = req.read().decode('utf-8')
        data = json.loads(data)
        location_utils.POI_CATEGORIES = dict()
        for category in data['poiCategories']:
            location_utils.POI_CATEGORIES[category['name']] = category['id']
        return location_utils.POI_CATEGORIES

    def get_location_series(address_series):
        lat_series = []
        lng_series = []
        for address in address_series:
            if address:
                lat, lng = location_utils.get_location(address)
            else:
                lat, lng = None, None
            lat_series.append(lat)
            lng_series.append(lng)
        return pd.Series(lat_series), pd.Series(lng_series)

print(location_utils.get_POI_categories())