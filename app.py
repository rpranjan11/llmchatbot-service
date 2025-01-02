import uvicorn
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'ollama_llm')))

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from openapi.custom_chatgpt_api import get_chatgpt_file_response, get_chatgpt_custom_response
from openapi.generic_chatgpt_api import get_chatgpt_generic_response
from ollama_llm.custom_ollama_api import get_ollama_file_response
from ollama_llm.generic_ollama_api import get_ollama_generic_response

# Load environment variables from .env file
load_dotenv()

file_path = './pdf_files/' # Initialize file_path as './pdf_files/'
file_name = None  # Initialize file_name as None

async def save_and_summarize_pdf(request: Request):
    print("Request received for save_and_summarize_pdf : ", await request.form())

    global file_name # Declare file_name as global to modify the global variable

    # Retrieve the request data
    form_data = await request.form()
    pdf_file = form_data.get("pdf")
    # chatgpt_model = form_data.get("chatgpt_model") # Not required for now
    ollama_model = form_data.get("ollama_model")

    if pdf_file is None:
        return JSONResponse({"error": "No PDF file provided"}, status_code=400)
    
    # Save the PDF file to disk
    file_name = pdf_file.filename
    save_path = os.path.join("pdf_files", file_name)
    
    with open(save_path, "wb") as f:
        f.write(await pdf_file.read())

    
    chatgpt_response = get_chatgpt_file_response(file_path + file_name)
    ollama_response = get_ollama_file_response(ollama_model, file_path + file_name, None)

    return JSONResponse({"message": "PDF file uploaded successfully", "chatgptResponse": chatgpt_response, "ollamaResponse": ollama_response}, status_code=200)

def chatgpt_custom_response(request):
    print("Request received for chatgpt_custom_response : ", request.path_params)

    prompt = request.path_params['prompt']
    # model = request.path_params['model'] # Not required for now

    chatgpt_response = get_chatgpt_custom_response(prompt)

    return JSONResponse({"chatgptResponse": chatgpt_response}, status_code=200)

def chatgpt_generic_response(request):
    print("Request received for chatgpt_generic_response :", request.path_params)

    prompt = request.path_params['prompt']
    # model = request.path_params['model'] # Not required for now

    chatgpt_response = get_chatgpt_generic_response(prompt)

    return JSONResponse({"chatgptResponse": chatgpt_response}, status_code=200)

def ollama_custom_response(request):
    print("Request received for ollama_custom_response : ", request.path_params)

    prompt = request.path_params['prompt']
    model = request.path_params['model']

    ollama_response = get_ollama_file_response(model, file_path + file_name, prompt)

    return JSONResponse({"ollamaResponse": ollama_response}, status_code=200)

def ollama_generic_response(request):
    print("Request received for ollama_generic_response : ", request.path_params)

    prompt = request.path_params['prompt']
    model = request.path_params['model']

    ollama_response = get_ollama_generic_response(model, prompt)

    return JSONResponse({"ollamaResponse": ollama_response}, status_code=200)

# Define the route for receiving PDF files
routes = [
    Route("/uploadpdf", endpoint=save_and_summarize_pdf, methods=["POST"]),
    Route("/chatgptcustomresponse/{model}/{prompt}", endpoint=chatgpt_custom_response, methods=["GET"]),
    Route("/chatgptgenericresponse/{model}/{prompt}", endpoint=chatgpt_generic_response, methods=["GET"]),
    Route("/ollamacustomresponse/{model}/{prompt}", endpoint=ollama_custom_response, methods=["GET"]),
    Route("/ollamagenericresponse/{model}/{prompt}", endpoint=ollama_generic_response, methods=["GET"])
]

# Define the middleware for the Starlette app to allow CORS requests from any origin
middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]),
]

# Add the routes & middleware to the Starlette app
app = Starlette(routes=routes, middleware=middleware)

# Run the Starlette app with Uvicorn server on port 8930
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8930)