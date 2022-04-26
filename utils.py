import json
import os

import requests
from fastapi.encoders import jsonable_encoder
from pricing.pricing import price_marketplace


def calculate_items_prices(listing_request):
    default_margin = 0.1

    margin = listing_request['margin'] if listing_request['margin'] else default_margin

    results_df = price_marketplace(
        jsonable_encoder(listing_request), listing_request['marketplace'], margin
    )
    return json.loads(results_df)






#here return json data for specific listing_id
def get_listing_request(listing_id):

    # Opening JSON file
    try:
        with open('listingFile.json', 'r') as fcc_file:
            fcc_data = json.load(fcc_file)
            return fcc_data

    except Exception as e:
        return f"Error while getting items: {e}"