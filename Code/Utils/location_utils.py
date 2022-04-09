import pandas as pd
import geopandas as gpd
import geopy
import urllib.request
import urllib.parse
import json

class location_utils():

    API_KEY = "AhbvYTADoexgk9EW4R5SyOu92avR1sTw"
    POI_CATEGORIES = None
    POI_RELEVANT = {'RESTAURANT': 7315, 'HOSPITAL': 7321002, 'SHOP': 9361, 'AIRPORT': 7383, 'HOTEL/MOTEL': 7314, 'SCHOOL': 7372002, 'PLACE OF WORSHIP': 7339, 'TOURIST ATTRACTION': 7376, 'BUS STOP': 9942002, 'LAUNDRY': 9361045, 'PARK': 9362008, 'SHOPPING CENTER': 7373, 'FIRE STATION': 7392, 'LIBRARY': 9913, 'POLICE STATION': 7322, 'GAS STATION': 7311, 'BANK': 7328}
    def get_POI_categories():
        if location_utils.POI_CATEGORIES:
            return location_utils.POI_CATEGORIES
        with open('Data/POI_categories.json', 'r') as openfile:
            data = json.load(openfile)
        location_utils.POI_CATEGORIES = dict()
        for category in data['poiCategories']:
            location_utils.POI_CATEGORIES[category['name'].upper()] = category['id']
        return location_utils.POI_CATEGORIES

    def serialize_POI_categories():
        url = f"https://api.tomtom.com/search/2//poiCategories.json?key={location_utils.API_KEY}"
        data = location_utils.get_data(url)
        json_object = json.dumps(data, indent = 4)
        with open("Data/POI_categories.json", "w") as outfile:
            outfile.write(json_object)

    def get_POI_from_ID(poi_id):
        url = f"https://api.tomtom.com/search/2/place.json?entityID={urllib.parse.quote(poi_id)}&key={location_utils.API_KEY}"
        data = location_utils.get_data(url)
        return data['poi']

    def get_nearby_POIs(lat, lon):
        url = f"https://api.tomtom.com/search/2/nearbySearch/.json?key={location_utils.API_KEY}&lat={lat}&lon={lon}"
        data = location_utils.get_data(url)
        return data['results']
    
    def is_POI_relevant(poi, verbose=True):
        if verbose:
            print(f'{poi["poi"]["name"]}\nCategories: {poi["poi"]["categories"]}')
        category_names = list(location_utils.POI_RELEVANT.keys())
        for category in poi["poi"]['categories']:
            if category.upper() in category_names:
                return True
        return False
         
    def get_location(address):
        url = f'https://api.tomtom.com/search/2/geocode/{urllib.parse.quote(address)}.json?key={location_utils.API_KEY}'
        data = location_utils.get_data(url)
        return data['results'][0]['position']['lat'], data['results'][0]['position']['lon']

    def get_address_rating(address):
        lat, lon = location_utils.get_location(address)
        POIs = location_utils.get_nearby_POIs(lat, lon)
        score = sum([location_utils.is_POI_relevant(poi) for poi in POIs])
        return score

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

    def get_data(url):
        req = urllib.request.urlopen(url)
        data = req.read().decode('utf-8')
        data = json.loads(data)
        return data

# address = "Okhla Industrial Estate, Phase III, near Govind Puri Metro Station 110020"
# # lat, lon = location_utils.get_location(address)
# # print(lat, lon)
# # print(location_utils.get_nearby_POIs(lat, lon))
# # print(location_utils.get_POI_categories())
# print(location_utils.get_address_rating(address))