#!/usr/bin/python3
"""
    Return requested listings
"""
from flask_cors import CORS
from flask import request, abort, Flask, jsonify
from pymongo import MongoClient
import json
import pprint

app = Flask(__name__)
CORS(app)
app.url_map.strict_slashes = False

@app.route('/search/<zip_code>', methods=['GET', 'POST'])
def get_listings(zip_code=None):
    """
        Retrieves list of all queried restaurant objects
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client.guiscore
    my_list = []
    tips_dict = {}
    if request.method == 'GET':
        if zip_code is None:
            abort(400, "Zip code is missing")
        for listings in db.restaurants.find({"zip_code": zip_code}):
            listings['_id'] = str(listings['_id'])
            my_list.append(listings)
        for tips in db.tips.find({"zip_code": zip_code}):
            tips['_id'] = str(tips['_id'])
            tips_dict['tips_dict'] = tips
            my_list.append(tips_dict)
        if my_list is None:
            abort(400, "No results found")
        return jsonify(my_list)

@app.route('/search/<zip_code>/<price>', methods=['GET', 'POST'])
def get_listings_with_price(zip_code=None, price=None):
    """
        Retrieves all restaurants based on zip and price
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client.guiscore
    my_list = []
    tips_dict = {}

    if request.method == 'GET':
        if zip_code is None:
            abort(400, "Zip code is missing")
        if price is None:
            abort(400, "Price is missing")
        for listings in db.restaurants.find({"zip_code": zip_code, "price_range": int(price)}):
            listings['_id'] = str(listings['_id'])
            my_list.append(listings)
        for tips in db.tips.find({"zip_code": zip_code}):
            print('TIPS', tips);
            print('--------');
            tips['_id'] = str(tips['_id'])
            tips_dict['tips_dict'] = tips
            my_list.append(tips_dict)
        if my_list is None:
            abort(400, "No results found")
        return jsonify(my_list)

@app.route('/search/<zip_code>/<price_list>', methods=['GET', 'POST'])
def get_listing_price_list(zip_code=None, price_list=[]):
    """
        Retrieves all restaurants based on a zipcode and pricelist
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client.guiscore
    my_list = []

    if request.method == 'GET':
        if zip_code is None:
            abort(400, "Zip code is missing")
        if price_list is None:
            abort(400, "Price list is missing")
        for price in price_list:
            for listings in db.restaurants.find({"zip_code": zip_code, "price_range": int(price)}):
                listings['_id'] = str(listings['_id'])
                my_list.append(listings)
            if my_list is None:
                abort(400, "No results found")
        return jsonify(my_list)

if (__name__) == "__main__":
    app.run(host='0.0.0.0', port=5000)
