#!/usr/bin/python3

from foursquare_remove_trucks import get_foursquare
from zomato_name_addr import get_zomato
from pymongo import MongoClient
from pyzomato import Pyzomato
from geopy import geocoders
import pprint

pp = pprint.PrettyPrinter(indent=4)
def create_match_list(foursquare_list=[], zomato_list=[]):
#   pp.pprint(foursquare_list)
#   print("LEN-FS", len(foursquare_list))
#   print("----------ZOMATO")
#   pp.pprint(zomato_list)
#   print("LEN-Z", len(zomato_list))
    main_list = []
    match_list = []
    no_match_list = []

    for restaurant_fs in foursquare_list:
#print("REST", restaurant['location'])
        for restaurant_z in zomato_list:
            new_restaurant = {}
            if restaurant_fs['location'] == restaurant_z['location']:
                rating_fs = restaurant_fs['rating_weight'] * restaurant_fs['standard_rating']
                rating_z = restaurant_z['rating_weight'] * restaurant_z['standard_rating']
                total_rating_weight = restaurant_fs['rating_weight'] + restaurant_z['rating_weight']
                new_rating = rating_fs + rating_z
#main_rating = (rating_fs + rating_z) / (restaurant_fs['total_reviews'] + restaurant_z['total_reviews'])

#               print("New ", main_rating)
                new_total_reviews = restaurant_fs['total_reviews'] + restaurant_z['total_reviews']
                composite = round(((new_rating/total_rating_weight) * 100), 2)
                new_restaurant['location'] = restaurant_fs['location']
                new_restaurant['name'] = restaurant_fs['name']
                new_restaurant['total_reviews'] = new_total_reviews
                new_restaurant['composite'] = composite
                match_list.append(new_restaurant)
                foursquare_list.remove(restaurant_fs)
                zomato_list.remove(restaurant_z)
    count1 = 0
    for no_match_fs in foursquare_list:
        no_match_fs['composite'] = 0
        no_match_list.append(no_match_fs)
        count1+=1
    for no_match_z in zomato_list:
        no_match_z['composite'] = 0
        no_match_list.append(no_match_z)
        count1+=1
    main_list = match_list + no_match_list
    print(len(main_list))
    print(count1)
#print("LEN-FS-NEW", len(foursquare_list))
#   print("LEN-Z-NEW", len(zomato_list))
#   print("-------------MAIN")
#   pp.pprint(main_list)
    return main_list
#   print("LEN-MAIN", len(main_list))
if __name__ == "__main__":
    foursquare_list = get_foursquare()
    zomato_list = get_zomato()
    create_match_list(foursquare_list, zomato_list)
