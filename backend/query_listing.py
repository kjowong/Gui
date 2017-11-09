#!/usr/bin/python3

import sys
from pymongo import MongoClient

def query_listing(*args):
    """
        Function to query each record
        *args: takes in the arguments
    """

    # Connect to mongo database
    client = MongoClient('mongodb://localhost:27017/')
    db = client.guiscore

    # If there is only 1 argument, find the listing and print it
    if len(args) == 1:
        for doc in db.restaurants.find({'zip_code':'{}'.format(args[0])}):
            print(doc)
    # If there is more then 1 argument, find the record with price range and zip code
    elif len(args) > 1:
        for doc in db.restaurants.find({'zip_code':'{}'.format(args[0]),
                                      'price_range':int('{:d}'.format(
                                       int(args[1])))}):
            print(doc)
if __name__ == "__main__":
    query_listing(*sys.argv[1:])

