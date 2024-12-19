from .customollamafunction import *
from langchain_community.llms.ollama import Ollama
from langchain.prompts import PromptTemplate
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

chain = ""


def get_ollamallm_response_with_file(file):

    # Loading orca-mini from Ollama
    llm = Ollama(model="orca-mini", temperature=0)

    # Loading the Embedding Model
    embed = load_embedding_model(model_path="all-MiniLM-L6-v2")

    # loading and splitting the documents
    docs = load_pdf_data(file_path = file )
    documents = split_docs(documents=docs)

    # creating vectorstore
    vectorstore = create_embeddings(documents, embed)

    # converting vectorstore to a retriever
    retriever = vectorstore.as_retriever()

    # Creating the prompt from the template
    prompt = PromptTemplate.from_template(prompt_template)

    # Creating the chain
    # chain = load_qa_chain(retriever, llm, prompt)
    chain = load_summarize_chain(llm, chain_type="stuff")  # specific for summary generation

    prompt = "Write a summary within 1000 words"

    search = vectorstore.similarity_search(" ")
    summary = chain.run(input_documents=search, question=prompt)
    print('Summary : ', summary)
    
    # return get_response(prompt, chain)
    return summary





# file = "../PDFfiles/Ranjan.pdf"
# response = get_ollamallm_response_with_file(file)

# print('-----------------')
# print(get_ollamallm_response("Who is Ram Pratap Ranjan"))
# print('-----------------')
# print(get_ollamallm_response("In which year did Ram Pratap Ranjan graduated"))


