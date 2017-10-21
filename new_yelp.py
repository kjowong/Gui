#!/usr/bin/python3

from foursquare_remove_trucks import get_foursquare
from zomato_name_addr import get_zomato
from match_list import create_match_list
import requests, json
from pymongo import MongoClient
import pprint

def aggregate_yelp(main_list=[]):
    client_id = 'SQqV-EaSklWJV9089z-LRg'
    client_secret = 'QkIzkk76Lv3wOWKK8lSgU794edzjo96sKfFrDolT4c6hHWivZfoZU1WKDLof9WII'
    data = {'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret}
    token = requests.post('https://api.yelp.com/oauth2/token', data=data)
    access_token = token.json()['access_token']
    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'bearer %s' % access_token}
    if len(main_list) > 0:
        for item in main_list:
            print("---------")
            print("NAME", item['name'])
            print("LOCATION", item['location'])
            print("--------")
            params = {'term': item['name'],
                        'location': item['location'],
                        'limit': 1
                     }
            resp = requests.get(url=url, params=params, headers=headers)
            business_details = resp.json()['businesses']
            print("BUSINESS DETAILS", business_details)
            # Getting id to possibly pass into new endpoint: business/{id}
            for item in business_details:
                business_id = item.get('id')
                phone_num = item.get('phone')
                price = item.get('price')
                rating = item.get('rating')
                reviews_count = item.get('review_count')
                image = item.get('image_url')
                coordinates = item.get('coordinates')
                print("------------")
                print("ID: ", business_id, ", phone:", phone_num, ", price: ", price, ", rating: ", rating, ", image: ", image, ", reviews: ", reviews_count, ", coord: ", coordinates)

if __name__ == "__main__":
    foursquare_list = get_foursquare()
    zomato_list = get_zomato()
    main_list = create_match_list(foursquare_list, zomato_list)
    aggregate_yelp(main_list)
