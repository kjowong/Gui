#!/usr/bin/python3

import json, requests
from pymongo import MongoClient
from geopy import geocoders
import sys

def four_square():
    url = 'https://api.foursquare.com/v2/venues/explore'
    bing_key = "bNV4gwzuDF0BY7hRBr2D~SwYlwf_NvSxlbZ36oGsTdA~AthfnABkus6e2oSBb4W9Q9_7yHrFh1cHbreVFmsPad2apAgjYqLYZi8E2iSyiJk-"
    bing = geocoders.Bing(bing_key)
    params = dict(
        client_id='ODAOUA2ZUGYKSAQMGSED4HVLAGQJZF4LU1FNEESGR2KY20CL',
        client_secret='TBGFJYKBYEUHORFJH3MCBB2DKP1SFBJ4ZUK2T3TVHGKBIHYD',
        v='20171110',
        near = 'San Francisco, CA',
        section = 'food',
        limit = 50
    )

    yelp_params = []

    r = requests.get(url=url, params=params).json()
    fs_list = (r.get('response').get('groups'))
    for post in fs_list:
        posts = (post.get('items'))
        for place in posts:
            restaurant = {}
            name = place.get('venue').get('name')
            street = place.get('venue').get('location').get('address')
            city = (place.get('venue').get('location').get('formattedAddress')[1]).replace(",", "")[:-5]
            address = street + " " +  city
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
                pass
    return yelp_params

if __name__ == "__main__":
    four_square()
