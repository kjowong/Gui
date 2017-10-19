#!/usr/bin/python3

import json, requests
from pymongo import MongoClient
from pyzomato import Pyzomato
import sys
from geopy import geocoders


if __name__ == "__main__":
    url = 'https://api.foursquare.com/v2/venues/explore'
    bing_key = "bNV4gwzuDF0BY7hRBr2D~SwYlwf_NvSxlbZ36oGsTdA~AthfnABkus6e2oSBb4W9Q9_7yHrFh1cHbreVFmsPad2apAgjYqLYZi8E2iSyiJk-"
    bing = geocoders.Bing(bing_key)
    params = dict(
        client_id='ODAOUA2ZUGYKSAQMGSED4HVLAGQJZF4LU1FNEESGR2KY20CL',
        client_secret='TBGFJYKBYEUHORFJH3MCBB2DKP1SFBJ4ZUK2T3TVHGKBIHYD',
        v='20171110',
        ll = '37.792085, -122.399368',
        section = 'food',
        limit = 15
)


    yelp_params = []

    r = requests.get(url=url, params=params).json()
    fs_list = (r.get('response').get('groups')) 
    for post in fs_list:
        posts = (post.get('items'))
        for place in posts:
            name = (place.get('venue').get('name'))
            print(name)
            address_field = place.get('venue').get('location')
            print(address_field)
            postal_code = address_field.get('postalCode')
            street = address_field.get('address')
            city = (address_field.get('formattedAddress')[1]).replace(",", "")[:-5]
            restaurant = {}
            try:
                address = street + " " +  city + " " + postal_code
                print("address", address)
            except:
                print("Removing from list\n")
                continue
            try:
                for place in bing.geocode(address, exactly_one=True):
                    location = ("%s" % (place))
                    if location is None:
                        restaurant['name'] = name
                        restaurant['location'] = address
                        yelp_params.append(restaurant)
                        print(address)
                    else:
                        restaurant['name'] = name
                        restaurant['location'] = location
                        yelp_params.append(restaurant)
                        print(location)
                        print("----------------------")
            except Exception as e:
                pass
        print(yelp_params)
