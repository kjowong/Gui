#!/usr/bin/python3

import json, requests
from pymongo import MongoClient
from geopy.geocoders import Nominatim
import sys

if __name__ == "__main__":

    url = 'https://api.foursquare.com/v2/venues/explore'
    params = dict(
        client_id='ODAOUA2ZUGYKSAQMGSED4HVLAGQJZF4LU1FNEESGR2KY20CL',
        client_secret='TBGFJYKBYEUHORFJH3MCBB2DKP1SFBJ4ZUK2T3TVHGKBIHYD',
        v='20171110',
        near = 'San Francisco, CA',
        section = 'food',
        limit = 50
)

    geolocator = Nominatim()

    r = requests.get(url=url, params=params).json()
    fs_list = (r.get('response').get('groups')) 
    for post in fs_list:
        posts = (post.get('items'))
        for place in posts:
            print(place.get('venue').get('name'))
            street = place.get('venue').get('location').get('address')
            city = (place.get('venue').get('location').get('formattedAddress')[1]).replace(",", "")[:-5]
            address = street + " " +  city
            try:
                location = geolocator.geocode(address)

                if location is None:
                    print(address)
                else:
                    print(location)
            except Exception as e:
                pass
