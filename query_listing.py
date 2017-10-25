#!/usr/bin/python3

import sys
from pymongo import MongoClient

def query_listing(*args):

    client = MongoClient('mongodb://localhost:27017/')
    db = client.guiscore
    if len(args) == 1:
        for doc in db.restaurants.find({'zip_code':'{}'.format(args[0])}):
            print(doc)
    elif len(args) > 1:
        for doc in db.restaurants.find({'zip_code':'{}'.format(args[0]),
                                      'price_range':int('{:d}'.format(
                                       int(args[1])))}):
            print(doc)
if __name__ == "__main__":
    query_listing(*sys.argv[1:])

