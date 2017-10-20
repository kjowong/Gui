#!/usr/bin/python3

import json, requests
from geopy import geocoders
from pyzomato import Pyzomato
import pprint

def get_zomato():
    bing_key = "bNV4gwzuDF0BY7hRBr2D~SwYlwf_NvSxlbZ36oGsTdA~AthfnABkus6e2oSBb4W9Q9_7yHrFh1cHbreVFmsPad2apAgjYqLYZi8E2iSyiJk-"
    bing = geocoders.Bing(bing_key)

    yelp_params = []

    p = Pyzomato('a27dcc3db4574a4ae90e9852091e736c')
    response = (p.getByGeocode(lan="37.792085", lon="-122.399368"))
    restaurants = (response.get('nearby_restaurants'))
    for place in restaurants:
        restaurant = {}
        info = place.get('restaurant')
        name = (info.get('name'))
        address = (info.get('location').get('address'))[:-1]
        rating = float(info.get('user_rating').get('aggregate_rating'))
        reviews_count = int(info.get('user_rating').get('votes'))
        restaurant['total_reviews'] = reviews_count
        standardized_rating = round((rating/5), 2)
        restaurant['standard_rating'] = standardized_rating
        rating_weight = round((reviews_count * 1.35), 2)
        restaurant['rating_weight'] = rating_weight
        try:
            for place in bing.geocode(address, exactly_one=False, timeout=3):
                location = str(place)
            if location is None:
                restaurant['name'] = name
                restaurant['location'] = address
                yelp_params.append(restaurant)
            else:
                restaurant['name'] = name
                restaurant['location'] = location
                yelp_params.append(restaurant)
        except Exception as e:
            print("ZERROR:", e)
    return yelp_params

if __name__ == "__main__":
    get_zomato()
