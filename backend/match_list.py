#!/usr/bin/python3

from foursquare_remove_trucks import get_foursquare
from zomato_name_addr import get_zomato
from pymongo import MongoClient
from pyzomato import Pyzomato
from geopy import geocoders
import pprint

def create_match_list(foursquare_list=[], zomato_list=[]):
    """
        Function that matches foursquare and zomato to pass to yelp
        foursquare_list: takes in list from foursquare, default empty
        zomato_list: takes in list from zomato, default empty
    """

    # Creates the empty list
    main_list = []
    match_list = []
    no_match_list = []

    # Iterate over foursquare and zomato lists
    for restaurant_fs in foursquare_list:
        for restaurant_z in zomato_list:
            new_restaurant = {}

            # If there is no location match, continue
            if restaurant_fs['location'] != restaurant_z['location']:
                continue

            # Standardize the rating score for foursquare and zomato
            rating_fs = restaurant_fs['rating_weight'] * restaurant_fs['standard_rating']
            rating_z = restaurant_z['rating_weight'] * restaurant_z['standard_rating']

            # Grab total rating weight of both foursquare and zomato
            total_rating_weight = restaurant_fs['rating_weight'] + restaurant_z['rating_weight']

            # New composite rating
            new_rating = rating_fs + rating_z

            # Total reviews combined
            new_total_reviews = restaurant_fs['total_reviews'] + restaurant_z['total_reviews']

            # Create new composite score
            composite = round(((new_rating/total_rating_weight) * 100), 2)

            # Update record with updated information
            new_restaurant['location'] = restaurant_fs['location']
            new_restaurant['name'] = restaurant_fs['name']
            new_restaurant['total_reviews'] = new_total_reviews
            new_restaurant['composite'] = composite
            new_restaurant['standard_rating'] = 0
            new_restaurant['rating_weight'] = 0
            new_restaurant['price_range'] = restaurant_fs['price_range']

            # Add match to new list and remove match from foursquare and zomato
            match_list.append(new_restaurant)
            foursquare_list.remove(restaurant_fs)
            zomato_list.remove(restaurant_z)

    # Appened the unmatched restaurants to unmatch list
    for no_match_fs in foursquare_list:
        no_match_fs['composite'] = 0
        no_match_list.append(no_match_fs)

    # Create new list from match and nomatch list
    main_list = match_list + no_match_list

    # Return the main list to pass
    return main_list

if __name__ == "__main__":
    create_match_list(foursquare_list, zomato_list)
