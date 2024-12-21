import uvicorn
import os
from dotenv import load_dotenv
import os

from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from OpenAPI.customchatgptapi import get_chatgpt_response_with_file, get_chatgpt_response
from OllamaLLM.ollamaapi import get_ollamallm_response
from OllamaLLM.customollamaapi import get_ollamallm_response_with_file

# Load environment variables from .env file
load_dotenv()

# app = Starlette()
#
# app.add_middleware(
#     CORSMiddleware, allow_origins=[os.getenv('MIDDLEWARE_ALLOW_ORIGIN_URL')], allow_headers=["*"], allow_methods=["*"]
# )

middleware = [
    Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]),
]

app = Starlette(routes=routes, middleware=middleware)

async def save_pdf(request: Request):

    # Retrieve the uploaded PDF file
    form_data = await request.form()
    pdf_file = form_data.get("pdf")
    
    if pdf_file is None:
        return JSONResponse({"error": "No PDF file provided"}, status_code=400)
    
    # Save the PDF file to disk
    filename = pdf_file.filename
    save_path = os.path.join("PDFfiles", filename)
    
    with open(save_path, "wb") as f:
        f.write(await pdf_file.read())

    
    chatgptresponse = get_chatgpt_response_with_file('./PDFfiles/' + filename)
    # ollamaresponse = get_ollamallm_response_with_file('./PDFfiles/' + filename)

    return JSONResponse({"message": "PDF file uploaded successfully", "chatgptresponse": chatgptresponse, "ollamaresponse": chatgptresponse}, status_code=200)

def get_chat_response(request, prompt : str = None):

    prompt = request.path_params['prompt']
    # model = request.query_params['model']

    # print('prompt : ', prompt)
    # if model == 'openapi':
    chatgptResponse = get_chatgpt_response(prompt)
    # elif model == 'ollamallm':
    #     ollamaresponse = get_ollamallm_response(prompt)

    return JSONResponse({"chatgptResponse": chatgptResponse}, status_code=200)

def get_ollama_response(request, prompt : str = None):

    prompt = request.path_params['prompt']
    # model = request.query_params['model']

    # print('prompt : ', prompt)
    # if model == 'openapi':
    # chatgptResponse = get_chatgpt_response(prompt)
    # elif model == 'ollamallm':
    ollamaresponse = get_ollamallm_response(prompt)

    return JSONResponse({"ollamaresponse": ollamaresponse}, status_code=200)


# Define the route for receiving PDF files
routes = [
    Route("/loadpdf", endpoint=save_pdf, methods=["POST"]),
    Route("/getchatresponse/{prompt}", endpoint=get_chat_response, methods=["GET"]),
    Route("/getllmresponse/{prompt}", endpoint=get_ollama_response, methods=["GET"]),
]

# Add the routes to the Starlette app
app.routes.extend(routes)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)