#!/usr/bin/python3

import json, requests
from geopy import geocoders
import sys
from pyzomato import Pyzomato
import pprint

if __name__ == "__main__":
    bing_key = "bNV4gwzuDF0BY7hRBr2D~SwYlwf_NvSxlbZ36oGsTdA~AthfnABkus6e2oSBb4W9Q9_7yHrFh1cHbreVFmsPad2apAgjYqLYZi8E2iSyiJk-"
    bing = geocoders.Bing(bing_key)

    pp = pprint.PrettyPrinter(indent=4)

    yelp_params = []

    p = Pyzomato('a27dcc3db4574a4ae90e9852091e736c')
    response = (p.getByGeocode(lan="37.792085", lon="-122.399368"))
    print("POPULARITY", response.get('popularity'))
    restaurants = (response.get('nearby_restaurants'))
    for place in restaurants:
        info = place.get('restaurant')
        print(info.get('user_rating').get('votes'), info.get('user_rating').get('aggregate_rating'))
        print("Price:  ", info.get('price_range'))
        name = (info.get('name'))
        print(name)
        address = (info.get('location').get('address'))[:-1]
        print("--------------------")
        restaurant = {}
        try:
            for place in bing.geocode(address, exactly_one=False):
                location = ("%s\n" % (place))
            if location is None:
                restaurant['name'] = name
                restaurant['location'] = address
                yelp_params.append(restaurant)
            else:
                restaurant['name'] = name
                restaurant['location'] = location
                yelp_params.append(restaurant)
        except Exception as e:
            print(e)
    print(yelp_params) 
