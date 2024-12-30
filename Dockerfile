# Stage 1: Python application setup
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
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

# Install Python dependencies
RUN python -m venv venv \
    && /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

# Preload the models using the `OllamaLLM` class
RUN python -c "from langchain_ollama import OllamaLLM; OllamaLLM(model='orca-mini', temperature=0); OllamaLLM(model='llama3.2', temperature=0)"

# Make port 8000 available to the outside world
EXPOSE 8000

# Define environment variable
ENV NAME LLMChatbot

# Define the entry point for the application
CMD ["venv/bin/python", "app.py"]