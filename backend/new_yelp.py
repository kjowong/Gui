#!/usr/bin/python3

from price_coord_passer import price_coord_func
from foursquare_remove_trucks import get_foursquare
from zomato_name_addr import get_zomato
from match_list import create_match_list
import requests, json
from pymongo import MongoClient
import pprint
import sys

def aggregate_yelp(main_list=[]):
    """
        Function to create the composite with yelp
        main_list: takes in the main list with matches and no matches
    """

    # Yelp credentials
    client_id = 'SQqV-EaSklWJV9089z-LRg'
    client_secret = 'QkIzkk76Lv3wOWKK8lSgU794edzjo96sKfFrDolT4c6hHWivZfoZU1WKDLof9WII'
    data = {'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret}
    token = requests.post('https://api.yelp.com/oauth2/token', data=data)
    access_token = token.json()['access_token']

    # Yelp endpoint
    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'bearer %s' % access_token}
    print(main_list)
    print("MAIN")

    # Empty list to fill in with yelp composites
    yelp_list = []

    # Only match with yelp if list passed in is not empty
    if main_list:
        for item in main_list:
            print("item", item)
            restaurant_with_composite = {}

            # Pass in the name and location from the main list into yelp
            params = {'term': item['name'],
                        'location': item['location'],
                        'limit': 1
                     }

            # Get the json response from yelp
            resp = requests.get(url=url, params=params, headers=headers)

            # Grab the business details from yelp
            business_details = resp.json()['businesses']
            print("------Getting Business Details in new_yelp.py__________")
            print("BUS - new_y.py", business_details)

            # If retaurant is not found in yelp, create the composite score without yelp
            if not business_details:
                item['composite'] = (item['standard_rating'] * 100)

            # If restaurant is found in yelp, grab necessary information
            if business_details:
                print("YES", item)
                for param in business_details:
                    business_id = param.get('id')
                    phone_num = param.get('phone')
                    price = param.get('price')
                    rating = param.get('rating')
                    reviews_count = param.get('review_count')
                    categories = param.get('categories')
                    cat_list = []
                    for title in categories:
                        cat_list.append(title.get('title'))
                    image = param.get('image_url')
                    coordinates = param.get('coordinates')

                # Calculating composite score for foursquare, zomato and yelp
                if item['composite'] != 0:
                    # Calculating composite score with zomato
                    print("ALREADY COMPARED", item)
                    composite_with_weight_fsz = (item['total_reviews'] * item['composite'] * 1.7)
                    yelp_composite_fsz = (reviews_count * 1.3 * (rating/5) * 100)
                    yelp_fsz_add = composite_with_weight_fsz + yelp_composite_fsz
                    total_fsz_reviews = (item['total_reviews'] * 1.7)
                    total_yelp_reviews = (reviews_count * 1.3)
                    yelp_reviews_divider = total_fsz_reviews + total_yelp_reviews
                    new_composite_fszy = (yelp_fsz_add / yelp_reviews_divider)
                    item.update({"phone_num":"{}".format(phone_num)})
                    item.update({"image_url":"{}".format(image)})
                    item.setdefault('categories', cat_list)
                    item['composite'] = round(new_composite_fszy, 2)
                    print("COMP-FSZY", item['composite'])
                    print("------------")
                    item['total_reviews'] = reviews_count + item['total_reviews']
                else:
                    # Calculating composite score without zomato
                    print("NO COMPO", item)
                    foursquare_composite = (item['standard_rating'] * item['total_reviews'] * 1.6)
                    yelp_composite = ((rating/5) * reviews_count * 1.4)
                    foursquare_reviews_weight = (item['total_reviews'] * 1.6)
                    item.update({"phone_num":"{}".format(phone_num)})
                    item.update({"image_url":"{}".format(image)})
                    item.setdefault('categories', cat_list)
                    yelp_reviews_weight = (reviews_count * 1.4)
                    foursquare_yelp_add = (foursquare_composite + yelp_composite)
                    yelp_reviews_fs_divider = (foursquare_reviews_weight + yelp_reviews_weight)
                    new_composite_fsy = ((foursquare_yelp_add / yelp_reviews_fs_divider) * 100)
                    item['composite'] = round(new_composite_fsy, 2)
                    print("FSY", item['composite'])
                    print("------------")
                    item['total_reviews'] = (item['total_reviews'] + reviews_count)
            # Update yelp list to the main list
            yelp_list = main_list
            print("YELP_LIST", yelp_list)
        # Return the created yelp list
        return yelp_list
    # If the main list passed is empty, just return
    else:
        print("--------------Print if empty yelp list from new_yelp.py-------------")
        return yelp_list

if __name__ == "__main__":
    args = price_coord_func(*sys.argv[1:])
    price = args[0]
    coords = args[1]
    foursquare_list = get_foursquare(price, latitude = coords.get('latitude'), longitude = coords.get('longitude'))
    zomato_list = get_zomato()
    main_list = create_match_list(foursquare_list, zomato_list)
    aggregate_yelp(main_list)
