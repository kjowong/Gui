#!/usr/bin/python3

import sys
from geopy import geocoders

def price_coord_func(zip_var, price_tier):

    bing_key = "bNV4gwzuDF0BY7hRBr2D~SwYlwf_NvSxlbZ36oGsTdA~AthfnABkus6e2oSBb4W9Q9_7yHrFh1cHbreVFmsPad2apAgjYqLYZi8E2iSyiJk-"
    geolocator = geocoders.Bing(bing_key)
    coordinates = {}

    location = geolocator.geocode(zip_var)
    coordinates['latitude'] = location.latitude
    coordinates['longitude'] = location.longitude
    return(price_tier, coordinates)

if __name__ == '__main__':
    price_coord_func(*sys.argv[:])
