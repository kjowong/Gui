#!/usr/bin/python3
"""Return requested listings"""
from flask import request, abort
from pymongo import MongoClient
import json
from flask import Flask, request

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/get_listing/<int:zip_code>/<int:price>')
def get_listings(zip_code=None, price=None):
    """Retrieves list of all queried restaurant objects""" 
    print(zip_code, price)
    client = MongoClient('mongodb://localhost:27017/')
    db = client.guiscore
    if zip_code is not None and price is None:
        for doc in db.restaurants.find({'zip_code':'{}'.format(zip_code)}):
            return(doc.get('name'), doc.get('composite'), doc.get('location'))
    elif price is not None:
        for doc in db.restaurants.find({'zip_code':'{}'.format(zip_code),
                                      'price_range':int('{:d}'.format(
                                       int(price)))}):
            return(doc.get('name'), doc.get('composite'), doc.get('location'), '\n')



if (__name__) == "__main__":
    app.run(host='0.0.0.0', port=5000) 
