#!/usr/bin/python3
"""Return requested listings"""
from flask import request, abort, Flask, jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/get_listing')
def get_listings():
    """Retrieves list of all queried restaurant objects""" 
    client = MongoClient('mongodb://localhost:27017/')
    db = client.guiscore
    my_list = []
 
    for listings in db.restaurants.find({"zip_code" : "94965"}):
        my_list.append(listings)
    return json.dumps(my_list)
    # if zip_code is not None and price is None:
    #     for doc in db.restaurants.find({'zip_code':'{}'.format(zip_code)}):
    #         return(doc.get('name'), doc.get('composite'), doc.get('location'))
    # elif price is not None:
    #     for doc in db.restaurants.find({'zip_code':'{}'.format(zip_code),
    #                                   'price_range':int('{:d}'.format(
    #                                    int(price)))}):
    #         return(doc.get('name'), doc.get('composite'), doc.get('location'), '\n')
    return("TEST") 

if (__name__) == "__main__":
    app.run(host='0.0.0.0', port=5000) 
