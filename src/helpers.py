import json
import os
import secrets
from pricecharting import IMAGE_DETAILS
from enum import IntEnum
from collections import defaultdict
from datetime import datetime
from typing import Any


# Gemini questions
class Gemini_Messages:
    WHAT_IS_IMG = 'What is the item in focus in this image?'

# HANDLING REQUESTS
# --------------------------------------------------

class CONTENT_TYPES(IntEnum):
    IMAGE = 0
    TEXT = 1

class SERVER_CONSTANTS:
    JSON_IMAGE_DATA = 'image_data'
    SAVING_IMAGE_RETRIES = 3

class SERVER_ROUTES:
    UPLOAD_IMAGE = '/upload_image'

# Content properties can contain details about the image / video uploaded as a dict
def handle_successful_http(server_route: str, content_properties=None):
    response_json = defaultdict(lambda: "")
    response_code = 200
    if server_route == SERVER_ROUTES.UPLOAD_IMAGE:
        response_json = {
            "message": "successfully handled image upload for processing",
            "date": str(datetime.now()) # might need to format data here
        }
        if content_properties:
            for key, value in content_properties.items():
                response_json[key] = value
        response_code = 202
    return json.dumps(response_json), response_code

IMAGE_DETAILS_KEYS = [IMAGE_DETAILS.ITEM_NAME, IMAGE_DETAILS.PRICE_LISTED, IMAGE_DETAILS.OTHER_DETAILS]
def parse_image_data_request(json_string: str) -> defaultdict[Any, None] | None:
    try:
        request_body_json = json.loads(json_string)
        dict_of_details = defaultdict(lambda: None)
        for key in IMAGE_DETAILS_KEYS:
            dict_of_details[key] = request_body_json[key]
        return dict_of_details
    except Exception as exc:
        print(f'Error parsing json for image data details with exc: {exc}')
        return None


# TODO set up proper error handling, codes and messages
ERROR_MSG = {
    "Invalid image sent"
}

ERROR_DETAILS = {
    "Expected image to be sent in format" # TODO insert specific format type expected here
}

def handle_unsuccessful_http(server_route: str, error_type: int, content_properties=None):
    response_json = defaultdict(lambda: "")
    if server_route == SERVER_ROUTES.UPLOAD_IMAGE:
        response_json = {
            "error": ERROR_MSG[error_type],
            "details": ERROR_DETAILS[error_type]
        }

    return json.dumps(response_json)

# Other helpful methods
# --------------------------------------------------
def update_filepath_for_saving(filepath: str):
    filepath_parts = filepath.split('.')
    filepath_exists = True
    while filepath_exists:
        random_tag = str(secrets.token_hex(5))
        new_filepath = filepath_parts[0] + random_tag + '.' + filepath_parts[1]
        if not os.path.isfile(new_filepath):
            filepath = new_filepath
            filepath_exists = False

    return filepath