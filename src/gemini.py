import os.path
import yaml
from helpers import CONTENT_TYPES
from google import genai

PARENT_DIRECTORY = os.getcwd()
CONFIG_YAML_PATH = PARENT_DIRECTORY + '\\resources\\config.yaml'
GEMINI_MODEL = 'gemini-2.5-flash'

# Setup
def get_config_yaml():
    print(CONFIG_YAML_PATH)
    try:
        with open(CONFIG_YAML_PATH, 'r') as file:
            yaml_data = yaml.full_load(file)
            return yaml_data
    except Exception as exc:
        print(f'Unhandled Exception obtaining yaml file {exc}')
        raise

API_KEY = str(get_config_yaml().get('apikey')['value'])

def setup() -> genai.Client:
    # https://ai.google.dev/gemini-api/docs/quickstart#python_1
    os.environ['GEMINI_API_KEY'] = API_KEY
    gemini_client = genai.Client()
    return gemini_client

def execute(gemini_client: genai.Client):
    print('Gemini client is loaded and waiting:')
    response = prompt_gemini_and_get_response(gemini_client, 'who is batman?')
    print(response)
    print(response.text)

# https://ai.google.dev/gemini-api/docs/image-understanding
def prompt_gemini_and_get_response(gemini_client: genai.Client, prompt: str, data, content_type: CONTENT_TYPES) -> genai.types.GenerateContentResponse:
    response = None
    contents = None
    model = GEMINI_MODEL
    if content_type == CONTENT_TYPES.TEXT:
        contents = prompt
    # in this case data would be image bytes
    if content_type == CONTENT_TYPES.IMAGE:
        contents = [
            genai.types.Part.from_bytes(
                data=data,
                mime_type='image/jpeg'
            ),
            prompt
        ]
    response = gemini_client.models.generate_content(model=model, contents=contents)
    return response