import os
import gemini # my personal python, possibly rename
from flask import Flask, request

from src.helpers import CONTENT_TYPES

UPLOAD_FOLDER = os.getcwd() + '\\assets\\uploaded'
print(os.getcwd())
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# TODO google search - making a POST request with an image in flutter
@app.route('/upload_image', methods=['POST', 'PUT'])
def upload_image():
    # check if the post request has the file part
    if 'file' not in request.files:
        return 'no file object'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return f'Image uploaded successfully: {file.filename}'

def set_image_details_from_gemini(image_filepath_name):
    with open(image_filepath_name, 'rb') as f:
        image_bytes = f.read()
    # TODO make the call to gemini api here
    response = gemini.prompt_gemini_and_get_response(gemini_client, 'What is this image?', image_bytes, CONTENT_TYPES.IMAGE)
    print(response.text)
    # TODO Continue from here
    return response.text


@app.route("/images/<image_id>", methods=['GET'])
def get_image_details(image_id):
    if request.method != 'GET':
        return 'incorrect http method'
    # TODO sql command to retrieve image data

if __name__ == '__main__':
    gemini_client = gemini.setup()
    gemini.execute(gemini_client)