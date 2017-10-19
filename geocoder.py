#!/usr/bin/python3
from yelp import four_square

import requests, json
from pymongo import MongoClient
import pprint

if __name__ == "__main__":

# lat/long for 800m distance from Embarcadero

    latitude = "37.7933"
    longitude = "-122.3975"
    client_id = "7kuhXsBS19IHvGwMrAxQ"
    client_code = "wWtPTFqP74cUDKe2LAoRMg"
    radius = "800"
    url = "https://reverse.geocoder.cit.api.here.com/6.2/reversegeocode.json?prox={}%2C%20{}%2C%20{}&mode=retrieveLandmarks&app_id={}&app_code={}&gen=9".format(latitude, longitude, radius, client_id, client_code)
    resp = requests.get(url=url)
    landmarks_list = resp.json()['Response']['View'][0]['Result']

    for landmark in landmarks_list:
#        pprint.pprint(landmark)
        print("-------")
        distance = landmark['Distance']
        name = landmark['Location']['Name']
        coordinates = landmark['Location']['DisplayPosition']
        print("-------")
        print("DIS", distance)
        print("NAME", name)
        print("COORD", coordinates)
