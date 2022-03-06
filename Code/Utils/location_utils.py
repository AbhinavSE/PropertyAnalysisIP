import pandas as pd
import geopandas as gpd
import geopy
import geocoder

#Parameters
PROJECT_NAME = "PropertyDataAnalysis"
API_KEY = "AhbvYTADoexgk9EW4R5SyOu92avR1sTw"

def get_location(address):
    g = geocoder.tomtom(address, key=API_KEY)
    return g.latlng

def get_location_series(address_series):
    location_series = pd.Series()
    for address in address_series:
        location_series.append(get_location(address))
    return location_series