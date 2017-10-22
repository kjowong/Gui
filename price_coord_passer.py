#!/usr/bin/python3

import sys
from geopy.geocoders import GoogleV3

def price_coord_func(zip_var, price_tier):

    geolocator = GoogleV3()
    coordinates = {}

    location = geolocator.geocode(zip_var)
    coordinates['latitude'] = location.latitude
    coordinates['longitude'] = location.longitude
    return(price_tier, coordinates)

if __name__ == '__main__':
    func_passer(*sys.argv[:])
