import os.path

import google.genai
import yaml
from google import genai

CONFIG_YAML_PATH = os.getcwd() + '\\resources\\config.yaml'
API_KEY = ''
GEMINI_MODEL = 'gemini-2.5-flash'

# Setup
def get_config_yaml():
    try:
        with open(CONFIG_YAML_PATH, 'r') as file:
            yaml_data = yaml.full_load(file)
            return yaml_data
    except Exception as exc:
        print(f'Unhandled Exception obtaining yaml file {exc}')

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

def prompt_gemini_and_get_response(gemini_client: genai.Client, prompt: str) -> genai.types.GenerateContentResponse:
    response = gemini_client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
    return response

if __name__ == '__main__':
    gemini_client = setup()
    execute(gemini_client)