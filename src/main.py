import os
import gemini # my personal python file, possibly rename
import socket
from flask import Flask, request
from flask_cors import CORS

import helpers
from helpers import CONTENT_TYPES

UPLOAD_FOLDER = os.getcwd() + '\\assets\\uploaded'
print(os.getcwd())
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MEGABYTE = 1024 * 1024
app.config['MAX_CONTENT_LENGTH'] = 10 * MEGABYTE
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Fix image too large error
@app.errorhandler(413)
def request_entity_too_large(error):
    return 'Image file is too large for processing, must be 8MB or below', 413

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# TODO google search - making a POST request with an image in react native
@app.route('/upload_image', methods=['POST', 'PUT'])
def upload_image():
    # check if the post request has the file part
    if 'image' not in request.files:
        return 'No file object sent', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return f'Image uploaded successfully for processing: {file.filename}', 202

def set_image_details_from_gemini(image_filepath_name):
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

GOOGLE_DNS = "8.8.8.8"
def get_local_ip_address():
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((GOOGLE_DNS, 80))
        return s.getsockname()[0] # should be the local ip address of this machine
    except Exception as exc:
        print(f'Exception occurred trying to connect to google\'s DNS server to get localip: {exc}')
        raise

LOCAL_PRIVATE_IP_ADDRESS = get_local_ip_address()
LISTENING_PORT = 5000

if __name__ == '__main__':
    gemini_client = gemini.setup()
    # TODO Set up certificate for security?
    app.run(host=LOCAL_PRIVATE_IP_ADDRESS, port=LISTENING_PORT, debug=False)