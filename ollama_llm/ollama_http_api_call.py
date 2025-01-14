import httpx
import logging

logging.basicConfig(level=logging.DEBUG)  # Configure logging level

def get_ollama_generic_response(model, prompt):
    try:
        logging.debug(f"Requesting Ollama API with model: {model}, prompt: {prompt}")
        response = httpx.get(f'http://61.32.218.74:8930/ollamagenericresponse/{model}/{prompt}',  timeout=60.0)
        response.raise_for_status()  # Raise an exception for HTTP errors
        logging.debug(f"Response: {response.json()}")
        return response.json()['ollamaResponse']

    except httpx.TimeoutException as exc:
        logging.error(f"Request timed out after 60 seconds: {exc}")
    except httpx.RequestError as exc:
        logging.error(f"An error occurred while requesting {exc.request.url!r}.")
    except httpx.HTTPStatusError as exc:
        logging.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
    except ValueError as exc:  # For JSON parsing errors
        logging.error(f"Error parsing JSON response: {exc}")
    return None


def get_ollama_file_response(model, prompt):
    try:
        logging.debug(f"Requesting Ollama API with model: {model}, prompt: {prompt}")
        response = httpx.get(f'http://61.32.218.74:8930/ollamacustomresponse/{model}/{prompt}', timeout=60.0)
        response.raise_for_status()  # Raise an exception for HTTP errors
        logging.debug(f"Response: {response.json()}")
        return response.json()['ollamaResponse']

    except httpx.TimeoutException as exc:
        logging.error(f"Request timed out after 60 seconds: {exc}")
    except httpx.RequestError as exc:
        logging.error(f"An error occurred while requesting {exc.request.url!r}.")
    except httpx.HTTPStatusError as exc:
        logging.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
    except ValueError as exc:  # For JSON parsing errors
        logging.error(f"Error parsing JSON response: {exc}")
    return None