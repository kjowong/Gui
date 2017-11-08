#!/usr/bin/python3
from geopy.geocoders import GoogleV3
from pymongo import MongoClient
import requests, json
from pyzomato import Pyzomato

if __name__ == "__main__":
    zomato_key = "a27dcc3db4574a4ae90e9852091e736c"

    zomato = Pyzomato(zomato_key)
    geolocator = GoogleV3(api_key="AIzaSyDQ-1MWdP4V8LAqo4CJ6t1gHsa0FZos7aI")
    zip_codes = ['94130', '94133', '94111', '94123', '94129', '94121', '94118', '94115', '94109', '94108', '94104', '94105', '94102', '94103', '94158', '94107', '94110', '94114', '94117', '94124', '94134', '94112', '94127', '94131', '94116', '94132', '94122']
    client = MongoClient('mongodb://localhost:27017/')
    db = client.guiscore

    for zip_code in zip_codes:
        address = geolocator.geocode(zip_code)
        response = (zomato.getByGeocode(lan="{}".format(address.latitude), lon="{}".format(address.longitude)))
        area_stats = response.get('popularity')
        area_stats.update({'zip_code':'{}'.format(zip_code)})
        print("------Adding Zomato area stats----------", area_stats)
        db.tips.insert(area_stats)
