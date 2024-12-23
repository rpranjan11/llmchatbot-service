import uvicorn
from dotenv import load_dotenv
import os

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from openapi.custom_chatgpt_api import get_chatgpt_response_from_file, get_chatgpt_custom_response
from openapi.generic_chatgpt_api import get_chatgpt_generic_response
from ollama.generic_ollama_api import get_ollama_generic_response
from ollama.custom_ollama_api import get_ollama_response_from_file

# Load environment variables from .env file
load_dotenv()

file_name = None # Initialize file_name as None
file_path = './pdf_files/' # Initialize file_path as './pdf_files/'

async def save_and_summarize_pdf(request: Request):

    # Retrieve the request data
    form_data = await request.form()
    pdf_file = form_data.get("pdf")
    model = form_data.get("model")
    
    if pdf_file is None:
        return JSONResponse({"error": "No PDF file provided"}, status_code=400)
    
    # Save the PDF file to disk
    file_name = pdf_file.file_name
    save_path = os.path.join("pdf_files", file_name)
    
    with open(save_path, "wb") as f:
        f.write(await pdf_file.read())

    
    chatgpt_response = get_chatgpt_response_from_file(file_path + file_name)
    ollama_response = get_ollama_response_from_file(model, file_path + file_name, None)

    return JSONResponse({"message": "PDF file uploaded successfully", "chatgptResponse": chatgpt_response, "ollamaResponse": ollama_response}, status_code=200)

def chatgpt_custom_response(request):

    prompt = request.path_params['prompt']

    chatgpt_response = get_chatgpt_custom_response(prompt)

    return JSONResponse({"chatgptResponse": chatgpt_response}, status_code=200)

def chatgpt_generic_response(request):

    prompt = request.path_params['prompt']

    chatgpt_response = get_chatgpt_generic_response(prompt)

    return JSONResponse({"chatgptResponse": chatgpt_response}, status_code=200)

def ollama_custom_response(request):

    prompt = request.path_params['prompt']
    model = request.path_params("model")

    ollama_response = get_ollama_response_from_file(model, file_path + file_name, prompt)

    return JSONResponse({"ollamaResponse": ollama_response}, status_code=200)

def ollama_generic_response(request):

    prompt = request.path_params['prompt']
    model = request.path_params("model")

    ollama_response = get_ollama_generic_response(model, prompt)

    return JSONResponse({"ollamaResponse": ollama_response}, status_code=200)

# Define the route for receiving PDF files
routes = [
    Route("/uploadpdf", endpoint=save_and_summarize_pdf, methods=["POST"]),
    Route("/chatgptcustomresponse/{prompt}", endpoint=chatgpt_custom_response, methods=["GET"]),
    Route("/chatgptgenericresponse/{prompt}", endpoint=chatgpt_generic_response, methods=["GET"]),
    Route("/ollamacustomresponse/{model}{prompt}", endpoint=ollama_custom_response, methods=["GET"]),
    Route("/ollamagenericresponse/{model}{prompt}", endpoint=ollama_generic_response, methods=["GET"])
]

# Define the middleware for the Starlette app to allow CORS requests from any origin
middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]),
]

# Add the routes & middleware to the Starlette app
app = Starlette(routes=routes, middleware=middleware)

# Run the Starlette app with Uvicorn server on port 8000
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)