# Description: Dockerfile for the LLMChatbot

# Use the official Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app
COPY . /app

# Install the dependencies in the container
RUN python -m venv venv \
    && . venv/bin/activate \
    && pip install ollama \
    && ollama \
    && ollama pull orca-mini \
    && ollama pull llama3.2

# Install the dependencies in the container
RUN pip install --no-cache-dir -r requirements.txt

# Run the LLM models
RUN python -c "from langchain_ollama import OllamaLLM; OllamaLLM(model='orca-mini', temperature=0); OllamaLLM(model='llama3.2', temperature=0)"

# Inform Docker that the container listens on the specified network ports at runtime
EXPOSE 8000
ENV NAME LLMChatbot

# Run the application
CMD ["venv/bin/python", "app.py"]