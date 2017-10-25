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
    client = MongoClient('mongodb://localhost:27017/')
    db = client.guiscore

    if len(yelp_list) > 0 and not None:
        for listing in yelp_list:
            print("------------Adding to database-----------------FROM DATABASE.PY")
            print("ARG1 - DB.py", args[0])
            print("------")
            print("ARG2 - DB.py", args[1])
            match_key = {}
            print("REST DB.py", listing.get('location'))
            match_key['location'] = listing.get('location')
            match_key['name'] = listing.get('name')
            print("NAME DB.py", listing.get('name'))
            result = db.restaurants.update(match_key, listing, upsert=True)

if __name__ == "__main__":
    zip_codes = ['94129', '94121', '94118']
#zip_codes = ['94130', '94133', '94111', '94123', '94129', '94121', '94118', '94115', '94109', '94108', '94104', '94105', '94102', '94103', '94158', '94107', '94110', '94114', '94117', '94124', '94134', '94112', '94127', '94131', '94116', '94132', '94122']
#price_range = ['1', '2', '3', '4']
    price_range = ['1', '2']
    for zip_code in zip_codes:
        for price in price_range:
            current_date = datetime.now().strftime('%Y-%m-%d')
            zip_dict = {}
            date_obj = {}
            zip_dict['zip_code'] = zip_code
            date_obj['updated_at'] = str(current_date)
            args = price_coord_func(zip_code, price)
            price = args[0]
            coords = args[1]
            foursquare_list = get_foursquare(price, latitude = coords.get('latitude'), longitude = coords.get('longitude'))
            zomato_list = get_zomato()
            main_list = create_match_list(foursquare_list, zomato_list)
            yelp_list = aggregate_yelp(main_list)
            for listing in yelp_list:
                listing.update(zip_dict)
                listing.update(date_obj)
            create_database(yelp_list, zip_code, price)
