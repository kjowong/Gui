#!/usr/bin/python3

import sys
from geopy.geocoders import GoogleV3

def price_coord_func(*args):

    geolocator = GoogleV3()
    coordinates = {}
    zip_code = args[0]
    if len(sys.argv) > 1:
        price = args[1]

    location = geolocator.geocode(zip_code)
    coordinates['latitude'] = location.latitude
    coordinates['longitude'] = location.longitude
    return(price, coordinates)

if __name__ == '__main__':
    func_passer(*sys.argv[:])
