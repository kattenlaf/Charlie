import time

import requests
import helpers
import server_logger
import json

# TODO item name and price listed will be treated as is, other details maybe can do some type of semantic analysis on ithe comments provided
class IMAGE_DETAILS:
    ITEM_NAME = 'item_name'
    PRICE_LISTED = 'price_listed'
    ITEM_CONDITION = 'item_condition' # TODO drop down on front end - great, good, ok, mediocre, terrible
    OTHER_DETAILS = 'other_details'

# https://www.pricecharting.com/api-documentation

### CONSTANTS FOR PRICECHARTING API
"""
p_ - prefix for params for requests
"""
# TODO move to config file?
DOMAIN_URL = 'https://www.pricecharting.com/'
DOMAIN_URL_API = DOMAIN_URL + 'api/'
DEMO_TOKEN = 'c0b53bce27c1bdab90b1605249e600dc43dfd1d5'
PRODUCT_ENDPOINT = 'product'
OFFER_ENDPOINT = 'offer'

# offer constants
SOLD = 'sold'
AVAILABLE = 'available'


# response
STATUS = P_OFFER_STATUS = 'status' # success or error, if response obtained as expected
CONSOLE_NAME = 'console-name'
PRODUCT_NAME = 'product-name'

OFFERS = 'offers'

# Some needed shortcuts for api
PRODUCT_ENDPOINT_URL = DOMAIN_URL_API + PRODUCT_ENDPOINT
OFFER_ENDPOINT_URL = DOMAIN_URL_API + OFFER_ENDPOINT

# general params for https://www.pricecharting.com/api/<endpoint>?t=<token>&id=<product_id>
P_PRODUCT_ID, PRODUCT_ID = 'id' # specific id for each product
P_TOKEN = 't' # token needed for api

# params for
# /product GET request
P_UNIVERSAL_PRODUCT_CODE = 'upc' # https://www.pricecharting.com/api-documentation#api-product
P_QUERY = 'q'  # product name you want to search for


# /offer GET request
# p_offer_status = 'offer-status' # available, sold, ended, collection
P_BUYER = 'buyer' # each buyer has a specific id, can be obtained from offer listing, not sure if will need
P_CONSOLE = 'console' # each specific console type for games, i believe this is a code TODO check api doc to be sure
P_SORT = 'sort' # see api documentation on line 3
# Responses
CONDITION_STRING = 'condition-string'
PRICE = 'price'
SALE_TIME = 'sale-time' # TODO factor in inflation, other potential details

# /offer-details GET request
# TODO check documentation

class PriceChartingProduct:
    """
    Class representation of a product on price charting to help keep code flow clean
    """
    def __init__(self,  response_json, loose_price=None, new_price=None, release_date=None):
        self.console_name = response_json[CONSOLE_NAME]
        self.product_id = response_json[PRODUCT_ID]
        self.product_name = response_json[PRODUCT_NAME]
        # premium response from product api
        self.loose_price = loose_price
        self.new_price = new_price
        self.release_date = release_date
        # other important details, such as how much was the product launched for
        self.launch_price = None

# shortcuts to not type long class names everytime
PCP = PriceChartingProduct

# reminder, do this flow after AI has done its processing as well
def check_product_exists(image_data_details, retries=0):
    url = PRODUCT_ENDPOINT_URL + 's' # plural products for more results
    product_name = image_data_details[IMAGE_DETAILS.ITEM_NAME]
    params = {
        P_TOKEN : DEMO_TOKEN,
        P_QUERY : product_name
    }
    content = make_pricecharting_request(url, params, 0)
    if content:
        response_json = json.loads(content)
        if response_json[STATUS] != 'success':
            print(f'{response_json}')  # TODO handle query wasn't successful to check if product exists
            return None
        product = PCP(response_json)
        return product
    return None

MAX_OFFERS_NEEDED = 50
# example api call - https://www.pricecharting.com/api/offers?t=c0b53bce27c1bdab90b1605249e600dc43dfd1d5&id=6910&status=sold
def check_offer_listings(product: PriceChartingProduct, image_data_details):
    url = OFFER_ENDPOINT_URL + "s"
    params = {
        P_TOKEN : DEMO_TOKEN,
        P_OFFER_STATUS : SOLD
    }
    if product.product_id is not None or product.product_id != "":
        params[P_PRODUCT_ID] = product.product_id
    content = make_pricecharting_request(url,params)
    if content:
        response_json = json.loads(content)
        offers = response_json[OFFERS]
        condition = image_data_details['condition'] if image_data_details is not None else None
        # TODO add key condition on front end side for user to send, or if AI will gather these details load it into the dictionary
        valid_offers = []
        for i in range(len(offers)):
            offer = offers[i] # Should be a json representing the offer
            if condition is not None:
                # TODO verify how to match conditions further
                if offer[CONDITION_STRING] and offer[CONDITION_STRING] == condition:
                    valid_offers.append(offer)
            else:
                valid_offers.append(offer)
            if len(valid_offers) > MAX_OFFERS_NEEDED:
                break
        return valid_offers
    return None

def analyze_offers(valid_offers: list[dict]):
    """

    :param valid_offers: list of all the offers returned from querying pricecharting in json response format
    :return: some data based on the analysis of the offers, analyze data and return information based on condition of item
            and other important details TODO Expound here
    """
    # TODO implement further
    return None

def make_pricecharting_request(url, params, retries=0):
    try:
        response = requests.get(url, params=params)
        content = response.content.decode() # decodes utf-8
        if not content:
            print(f'no results for product on price charting based on information provided')
            return None
        return content
    except requests.exceptions.ConnectionError as exc:
        print(f'some network issue when making a request to pricecharting api: {exc}')
    except requests.exceptions.Timeout as exc:
        print(f'some timeout exception when making request to pricecharting api: {exc}')
        if retries < 3:
            time.sleep(20)
            retries += 1
            return make_pricecharting_request(url, params, retries)
        else:
            print(f'giving up making request to pricecharting api')
            return None
    except requests.exceptions.RequestException as exc:
        print(f'some request exception when making request to pricecharting api: {exc}')
    except Exception as exc:
        print(f'unexpected error during request/parsing response from price charting: {exc}')
    return None