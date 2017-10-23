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
    zip_codes = ['94130', '94133', '94111', '94123', '94129', '94121', '94118', '94115', '94109', '94108', '94104', '94105', '94102', '94103', '94158', '94107', '94110', '94114', '94117', '94124', '94134', '94112', '94127', '94131', '94116', '94132', '94122']
    price_range = ['1', '2', '3', '4', '1,2', '1,3', '1,4', '2,3', '2,4', '3,4', '1,2,3', '1,2,4', '1,3,4', '2,3,4', '1,2,3,4']
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
