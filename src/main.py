import os
import gemini # my personal python file, possibly rename
import socket
import asyncio
from flask import Flask, request, send_from_directory
from flask_cors import CORS

import helpers
from helpers import CONTENT_TYPES
from src.helpers import SERVER_ROUTES

UPLOAD_FOLDER = os.getcwd() + '\\assets\\uploaded\\images'
print(os.getcwd())
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MEGABYTE = 1024 * 1024
app.config['MAX_CONTENT_LENGTH'] = 10 * MEGABYTE
app.config['MAX_FORM_MEMORY_SIZE'] = 10 * MEGABYTE # FIXME: Unblocks the error where 413 is returned because of large file sent
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
GOOGLE_DNS = "8.8.8.8"

# Fix image too large error
@app.errorhandler(413)
def request_entity_too_large(error):
    return 'Image file is too large for processing, must be 8MB or below', 413

@app.route("/favicon.ico")
def favicon():
    try:
        print(app.root_path)
        favicon = send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')
    except Exception as e:
        print(f'Exception occurred loading the favicon {e}')
    return favicon

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# TODO google search - making a POST request with an image in react native
@app.route('/upload_image', methods=['POST', 'PUT'])
def upload_image():
    print(request.files)
    # check if the post request has the file part
    if 'image' not in request.files:
        print('no image')
        return 'No file object sent', 400
    print('image found')
    try:
        file = request.files.get('image')
    except Exception as e:
        print(f'Internal server exception loading image: {e}')
        return 'error loading received file on server', 500
    if file.filename == '':
        return 'No selected file', 400
    if file:
        # TODO parse image_data sent over from client here
        if request.form:
            if helpers.SERVER_MESSAGES_CONSTANTS.JSON_IMAGE_DATA in request.form:
                image_data_details = helpers.parse_image_data_request(request.form.get(helpers.SERVER_MESSAGES_CONSTANTS.JSON_IMAGE_DATA))
                print(image_data_details)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        # TODO introduce database to be able to find images with a given image id?
        if os.path.isfile(filepath):
            filepath = helpers.update_filepath_for_saving(filepath)
        file.save(filepath)
        # TODO after this file is saved put in some message queue or just queue to be picked up and processed by gemini
        # TODO or just send back the resutls?
        try:
            print(fetch_image_details_from_gemini(filepath))
        except Exception as e:
            print(f'Exception occurred requesting image status from gemini: {e}')
            return helpers.handle_unsuccessful_http(SERVER_ROUTES.UPLOAD_IMAGE)
        return helpers.handle_successful_http(SERVER_ROUTES.UPLOAD_IMAGE)

def fetch_image_details_from_gemini(image_filepath_name):
    with open(image_filepath_name, 'rb') as f:
        image_bytes = f.read()
    response = gemini.prompt_gemini_and_get_response(gemini_client, helpers.Gemini_Messages.WHAT_IS_IMG, image_bytes, CONTENT_TYPES.IMAGE)
    print(response.text)
    # TODO Continue from here
    return response.text


@app.route("/images/<image_id>", methods=['GET'])
def get_image_details(image_id):
    if request.method != 'GET':
        return 'incorrect http method'
    # TODO sql command to retrieve image data

def get_local_ip_address():
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((GOOGLE_DNS, 80))
        return s.getsockname()[0] # should be the local ip address of this machine
    except Exception as exc:
        print(f'Exception occurred trying to connect to google\'s DNS server to get local ip: {exc}')
        raise

LOCAL_PRIVATE_IP_ADDRESS = get_local_ip_address()
LISTENING_PORT = 5000

if __name__ == '__main__':
    gemini_client = gemini.setup()
    # TODO Set up certificate for security?
    app.run(host=LOCAL_PRIVATE_IP_ADDRESS, port=LISTENING_PORT, debug=False)