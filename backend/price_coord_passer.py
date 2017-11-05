#!/usr/bin/python3

import sys
from geopy import geocoders

def price_coord_func(zip_var, price_tier):
    """
        Function that coordinates the price with the zip codes
        zip_var: takes in the zip code
        price_tier: takes in the price range
    """

    # Bing key to use bing to standardized addresses
    bing_key = "bNV4gwzuDF0BY7hRBr2D~SwYlwf_NvSxlbZ36oGsTdA~AthfnABkus6e2oSBb4W9Q9_7yHrFh1cHbreVFmsPad2apAgjYqLYZi8E2iSyiJk-"
    geolocator = geocoders.Bing(bing_key)
    coordinates = {}

    location = geolocator.geocode(zip_var, timeout=5)

    # Update the coordinates with the lat and long returned
    coordinates['latitude'] = location.latitude
    coordinates['longitude'] = location.longitude

    # Return the price and coorindates
    return(price_tier, coordinates)

if __name__ == '__main__':
    price_coord_func(*sys.argv[:])
