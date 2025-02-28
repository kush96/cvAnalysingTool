import os
import configparser

cfgParser = configparser.ConfigParser()
cfgParser.read('config.ini')

ENV = os.getenv('ENV', 'DEFAULT')

if ENV not in cfgParser:
    raise ValueError(f"Environment '{ENV}' not found in config.ini")

config = cfgParser[ENV]

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError(f"OpenAI API Key Needed to start chatbot...closing down")
else:
    config['openai_api_key'] = OPENAI_API_KEY

