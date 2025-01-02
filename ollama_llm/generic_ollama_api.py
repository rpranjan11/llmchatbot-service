import ollama
import logging
import httpx

logging.basicConfig(level=logging.DEBUG)  # Configure logging level

def get_ollama_generic_response(model, prompt):
    try:
        logging.debug(f"Requesting Ollama API with model: {model}, prompt: {prompt}")

        response = ollama.chat(
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                }
            ],
            model=model
        )

        return response['message']['content']
    except httpx.ConnectError as e:
        logging.error(f"Connection error: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise


# model = "llama3.2"
# prompt = "Who is APJ Abdul Kalam"
# response = get_ollama_response(model, prompt)
# print('Ollama Api Response : ', response)
