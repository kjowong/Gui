#!/usr/bin/python3

from price_coord_passer import price_coord_func
from foursquare_remove_trucks import get_foursquare
from zomato_name_addr import get_zomato
from match_list import create_match_list
from new_yelp import aggregate_yelp
import requests, json
from pymongo import MongoClient
import pprint
from datetime import datetime
import sys

def create_database(yelp_list=[], *args):
    print("-----ZIP CODE: ", args[0], "------PRICE TIER: ", args[1])
    pprint.pprint(yelp_list)
#pprint.pprint(yelp_list)
#    print(datetime.now())
    
    # current_date = datetime.now()
    # client = MongoClient('mongodb://localhost:27017/')
    # current_date = str(current_date)
    # db = client.current_date
 


if __name__ == "__main__":
    zip_codes = ['94124', '94111', '94965']
    price_range = ['1', '2', '3']
    for zip_code in zip_codes:
        for price in price_range:
            zip_var = zip_code
            price_tier = price
            args = price_coord_func(zip_var, price_tier)
            price = args[0]
            coords = args[1]
            foursquare_list = get_foursquare(price, latitude = coords.get('latitude'), longitude = coords.get('longitude'))
            zomato_list = get_zomato()
            main_list = create_match_list(foursquare_list, zomato_list)
            yelp_list = aggregate_yelp(main_list)
            print(zip_var, price_tier)
            create_database(yelp_list, zip_var, price_tier)
