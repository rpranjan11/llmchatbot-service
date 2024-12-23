This is a ChatGpt and Ollama based real-time chat app where you can upload a pdf and query from the uploaded pdf OR you can ask any question and get the answer from the OpenAI API as well as Ollama API.

## Prerequisites
- Python 3.6 or higher
- pip

## To install the dependencies
pip install -r requirements.txt

## Before you run the app locally, add the below properties to the .env file in the root directory
OPENAPI_API_KEY=<api_key> # Get the api key from https://platform.openai.com/api-keys
OPENAPI_ASSISTANT_ID=<organisation_id> # Get the assistant id from https://platform.openai.com/assistants
MIDDLEWARE_ALLOW_ORIGIN_URL=<url> # The url of the frontend app

## To deploy on the server, add the below properties to the environment variables
OPENAPI_API_KEY=
OPENAPI_ASSISTANT_ID=
MIDDLEWARE_ALLOW_ORIGIN_URL=

## To run the app
python app.py
