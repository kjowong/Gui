#!/usr/bin/python3

import json, requests
from geopy import geocoders
from pyzomato import Pyzomato
import pprint
import os

ZOMATO_API_KEY = os.environ.get('ZOMATO_API_KEY')

def get_zomato():
    """
        Function to grab the restaurants from zomato
    """

    # Bing key to standardized the addresses
    bing_key = os.environ.get('BING_API_KEY')
    bing = geocoders.Bing(bing_key)

    # Empty list to add restaurants in
    yelp_params = []

    # Use Pyzomato to make requests to zomato api
    p = Pyzomato(ZOMATO_API_KEY)

    # Location response
    response = (p.getByGeocode(lan="37.792085", lon="-122.399368"))

    # Json response from zomato
    restaurants = (response.get('nearby_restaurants'))

    # Iterate over response and grab necessary information
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
        price_range = info.get('price_range')
        restaurant['price_range'] = price_range

        # Try to update the location with bing's addesss
        try:
            for place in bing.geocode(address, exactly_one=False, timeout=5):
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
    # Return the completed list
    return yelp_params

if __name__ == "__main__":
    get_zomato()
