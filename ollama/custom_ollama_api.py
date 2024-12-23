import os
from custom_ollama_function import *
from langchain_community.llms.ollama import Ollama
from langchain.chains.summarize import load_summarize_chain

prompt_template = """
### System:
You are an respectful and honest assistant. You have to answer the user's \
questions using only the context provided to you. If you don't know the answer, \
just say you don't know. Don't try to make up an answer.

### Context:
{context}

### User:
{question}

### Response:
"""

file = None  # Initialize file as None
chain = None  # Initialize chain as None
vectorstore = None  # Initialize vectorstore as None
prompt = None  # Initialize prompt as None
model = None  # Initialize model as None

def get_ollamallm_response_with_file(model, file, prompt):
    global chain, vectorstore  # Declare chain and vectorstore as global to modify the global variables

    # Loading the Ollama Model
    llm = Ollama(model=model, temperature=0)

    # Loading the Embedding Model
    embed = load_embedding_model(model_path="all-MiniLM-L6-v2")

    # loading and splitting the documents
    docs = load_pdf_data(file_path = file )
    documents = split_docs(documents=docs, chunk_size=500, chunk_overlap=50)  # Optimized chunk size and overlap

    # creating vectorstore
    vectorstore = create_embeddings(documents, embed)

    # converting vectorstore to a retriever
    retriever = vectorstore.as_retriever()

    # Creating the chain
    # chain = load_qa_chain(retriever, llm, prompt)
    if prompt is None:
        prompt = "Write a summary within 1000 words"
        chain = load_summarize_chain(llm, chain_type="stuff")  # specific for summary generation
        search = vectorstore.similarity_search(" ")
        summary = chain.invoke(input={"input_documents": search, "question": prompt})
        return summary['output_text']
    else:
        chain = load_qa_chain(retriever, llm, prompt)
        search = vectorstore.similarity_search(" ")
        response = chain.invoke(input={"input_documents": search, "query": prompt})
        return response['result']



file = "./PDFfiles/Ranjan.pdf"
if not os.path.isfile(file):
    raise ValueError(f"File path {file} is not a valid file or url")

# Loading orca-mini from Ollama
model = "orca-mini"
summary = get_ollamallm_response_with_file(model, file, prompt)
print('Summary : ', summary)
print('-----------------')

# Loading llama3.2 from Ollama
model = "llama3.2"
print('Response : ', get_ollamallm_response_with_file(model, file, "Who is Ranjan"))
print('-----------------')
print('Response : ', get_ollamallm_response_with_file(model, file, "In which year did Ram Pratap Ranjan graduated"))
print('-----------------')
print('Response : ', get_ollamallm_response_with_file(model, file, "Who is APJ Abdul kalam"))
