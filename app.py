import uvicorn
from dotenv import load_dotenv
import os
import sys
import httpx
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'ollama_llm')))

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from openapi.custom_chatgpt_api import get_chatgpt_file_response, get_chatgpt_custom_response
from openapi.generic_chatgpt_api import get_chatgpt_generic_response
from ollama_llm.ollama_http_api_call import get_ollama_file_response, get_ollama_generic_response

# Load environment variables from .env file
load_dotenv()

async def save_and_summarize_pdf(request: Request):
    print("Request received for save_and_summarize_pdf : ", await request.form())

    # Forward the request to the target server
    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
        try:
            form_data = await request.form()
            pdf_file = form_data["pdf"]

            # Ensure the file has a .pdf extension
            if not pdf_file.filename.lower().endswith('.pdf'):
                return JSONResponse(
                    {"error": "Only PDF files are supported"},
                    status_code=400
                )

            # Prepare the file with explicit filename
            files = {
                "pdf": (
                    pdf_file.filename,
                    await pdf_file.read(),
                    "application/pdf"
                )
            }
            data = {"ollama_model": form_data.get("ollama_model")}

            response = await client.post(
                "http://61.32.218.74:8930/uploadpdf",
                files=files,
                data=data
            )

            return JSONResponse(response.json(), status_code=response.status_code)

        except httpx.ReadTimeout:
            return JSONResponse(
                {"error": "Request timed out after 60 seconds"},
                status_code=504
            )

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

    ollama_response = get_ollama_file_response(model, prompt)

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

# Run the Starlette app with Uvicorn server on port 8000
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)