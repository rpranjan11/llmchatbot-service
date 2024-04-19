import uvicorn
import os

from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware
from OpenAPI.customchatgptapi import get_chatgpt_response_with_file, get_chatgpt_response
# from OllamLLM.ollamaapi import get_ollamallm_response

app = Starlette()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_headers=["*"], allow_methods=["*"]
)

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
    # ollamaresponse = get_chatgpt_response_with_file('../PDFfiles/' + filename + '.pdf')

    return JSONResponse({"message": "PDF file uploaded successfully", "chatgptresponse": chatgptresponse, "ollamaresponse": chatgptresponse}, status_code=200)

async def get_chat_response(self, request, prompt : str = None, model : str = None):

    prompt = request.path_params['prompt']
    model = request.path_params['model']

    print('Prompt : ', prompt)
    if model == 'openapi':
        chatgptResponse = get_chatgpt_response(prompt)
    # elif model == 'ollamallm':
    #     ollamaresponse = get_ollamallm_response(prompt)

    return JSONResponse({"message": chatgptResponse}, status_code=200)


# Define the route for receiving PDF files
routes = [
    Route("/loadpdf", endpoint=save_pdf, methods=["POST"]),
    Route("/getchatresponse", endpoint=get_chat_response, methods=["GET"]),
]

# Add the routes to the Starlette app
app.routes.extend(routes)