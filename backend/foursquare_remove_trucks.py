#!/usr/bin/python3

import json, requests
from pymongo import MongoClient
from geopy import geocoders
import pprint
import sys
from sys import argv
from price_coord_passer import price_coord_func

def get_foursquare(price, **kwargs):
    """
        Function that gets the foursquare restaurants
        Price: takes in the price range sent in
        *kwargs: takes in other arguments
    """

    # Foursquare endpoint and bing key to standardized addresses
    url = 'https://api.foursquare.com/v2/venues/explore'
    bing_key = "bNV4gwzuDF0BY7hRBr2D~SwYlwf_NvSxlbZ36oGsTdA~AthfnABkus6e2oSBb4W9Q9_7yHrFh1cHbreVFmsPad2apAgjYqLYZi8E2iSyiJk-"
    bing = geocoders.Bing(bing_key)

    # Foursquare parameters to pass into api
    params = dict(
        client_id='ODAOUA2ZUGYKSAQMGSED4HVLAGQJZF4LU1FNEESGR2KY20CL',
        client_secret='TBGFJYKBYEUHORFJH3MCBB2DKP1SFBJ4ZUK2T3TVHGKBIHYD',
        v='20171210',
        ll = '{}, {}'.format(kwargs.get('latitude'), kwargs.get('longitude')),
        section = 'food',
        limit = 5,
        price = price
    )

    # Empty list to add restaurants into
    yelp_params = []

    # Grabs the json response with requests
    r = requests.get(url=url, params=params).json()
    fs_list = (r.get('response').get('groups'))

    # For each restaurant in the returned foursquare list, grab necessary information
    for post in fs_list:
        posts = (post.get('items'))
        for place in posts:
            print("FOURSQUARE", place)
            name = (place.get('venue').get('name'))
            address_field = place.get('venue').get('location')
            postal_code = address_field.get('postalCode')
            street = address_field.get('address')
            city = (address_field.get('formattedAddress')[1]).replace(",", "")[:-5]
            restaurant = {}
            price_range = place.get('venue').get('price').get('tier')
            tips = place.get('tips')

            # Grabbing tips
            if tips is not None:
                for items in tips:
                    tip = items['text']
                if tip is not None:
                    restaurant['tip'] = tip

            # Grabbing rating
            rating = place.get('venue').get('rating')
            if (rating is None):
                break
            restaurant['price_range'] = price_range
            reviews_count = place.get('venue').get('ratingSignals')
            restaurant['zip_code'] = postal_code
            restaurant['total_reviews'] = reviews_count 
            standardized_rating = round((rating/10), 2)
            restaurant['standard_rating'] = standardized_rating
            rating_weight = round((reviews_count * 1.35), 2)
            restaurant['rating_weight'] = rating_weight

            # Attempting to create standard address
            try:
                address = street + " " +  city + " " + postal_code
            except:
                continue

            # Pass in address from foursquare, try to return bing address
            try:
                bing_location = bing.geocode(address, exactly_one=True, timeout=5)
                location = str(bing_location)
                if location is None:
                    restaurant['name'] = name
                    restaurant['location'] = address
                    yelp_params.append(restaurant)
                else:
                    restaurant['name'] = name
                    restaurant['location'] = location
                    yelp_params.append(restaurant)
            except Exception as e:
                print("ERROR", e)
        # Return the completed list
        return yelp_params

if __name__ == "__main__":
    args = price_coord_func(*sys.argv[1:])
    price = args[0]
    coords = args[1]
    get_foursquare(price, latitude = coords.get('latitude'), longitude = coords.get('longitude'))
