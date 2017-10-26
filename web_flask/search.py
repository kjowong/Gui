#!/usr/bin/python3
"""
    Return requested listings
"""
from flask import request, abort, Flask, jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/search/<zip_code>', methods=['GET', 'POST'])
def get_listings(zip_code=None):
    """
        Retrieves list of all queried restaurant objects
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client.guiscore
    my_list = []

    if request.method == 'GET':
        for listings in db.restaurants.find({"zip_code": zip_code}):
            listings['_id'] = str(listings['_id'])
            my_list.append(listings)
        if my_list is None:
            abort(400, "No results found")
        return jsonify(my_list)

@app.route('/search/<zip_code>/<price>', methods=['GET', 'POST'])
def get_listings_with_price(zip_code=None, price=None):
    """
        Retrieves all restaurants based on zip and pricec
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client.guiscore
    my_list = []

    if request.method == 'GET':
        for listings in db.restaurants.find({"zip_code": zip_code, "price_range": int(price)}):
            listings['_id'] = str(listings['_id'])
            my_list.append(listings)
        if my_list is None:
            abort("400", "No results found")
        return jsonify(my_list)

if (__name__) == "__main__":
    app.run(host='0.0.0.0', port=5000) 
