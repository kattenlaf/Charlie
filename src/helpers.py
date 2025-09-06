import json
import os
import secrets
from enum import IntEnum
from collections import defaultdict
from datetime import datetime

# Gemini questions
class Gemini_Messages:
    WHAT_IS_IMG = 'What is the item in focus in this image?'

# HANDLING REQUESTS
# --------------------------------------------------

class CONTENT_TYPES(IntEnum):
    IMAGE = 0
    TEXT = 1

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

    return json.dumps(response_json), 202

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