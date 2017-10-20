#!/usr/bin/python3

from foursquare_remove_trucks import get_foursquare
from zomato_name_addr import get_zomato
from pymongo import MongoClient
from pyzomato import Pyzomato
from geopy import geocoders
import pprint

pp = pprint.PrettyPrinter(indent=4)
def create_match_list(foursquare_list=[], zomato_list=[]):

    main_list = []
    match_list = []
    no_match_list = []

    for restaurant_fs in foursquare_list:
        for restaurant_z in zomato_list:
            new_restaurant = {}
            if restaurant_fs['location'] == restaurant_z['location']:
                rating_fs = restaurant_fs['rating_weight'] * restaurant_fs['standard_rating']
                rating_z = restaurant_z['rating_weight'] * restaurant_z['standard_rating']
                total_rating_weight = restaurant_fs['rating_weight'] + restaurant_z['rating_weight']
                new_rating = rating_fs + rating_z
                new_total_reviews = restaurant_fs['total_reviews'] + restaurant_z['total_reviews']
                composite = round(((new_rating/total_rating_weight) * 100), 2)
                new_restaurant['location'] = restaurant_fs['location']
                new_restaurant['name'] = restaurant_fs['name']
                new_restaurant['total_reviews'] = new_total_reviews
                new_restaurant['composite'] = composite
                new_restaurant['standard_rating'] = 0
                new_restaurant['rating_weight'] = 0
                match_list.append(new_restaurant)
                foursquare_list.remove(restaurant_fs)
                zomato_list.remove(restaurant_z)

    for no_match_fs in foursquare_list:
        no_match_fs['composite'] = 0
        no_match_list.append(no_match_fs)
    for no_match_z in zomato_list:
        no_match_z['composite'] = 0
        no_match_list.append(no_match_z)
    main_list = match_list + no_match_list
    return main_list
if __name__ == "__main__":
    create_match_list(foursquare_list, zomato_list)
