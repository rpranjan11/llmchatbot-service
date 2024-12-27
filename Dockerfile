# Stage 1: Base image for installing dependencies and Ollama
FROM ubuntu:22.04 AS base

# Install necessary tools
RUN apt-get update && apt-get install -y curl wget tar python3 python3-venv python3-pip docker.io

# Install Ollama
RUN curl -fsSL https://ollama.com/download | bash

# Pull the required models
RUN ollama pull llama3.2 \
    && ollama pull orca-mini

# Stage 2: Python application setup
FROM python:3.11-slim AS app

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install Python dependencies
RUN python -m venv venv \
    && /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

# Install the Ollama Python package
RUN /bin/bash -c "source venv/bin/activate && pip install ollama"

# Preload the models using the `OllamaLLM` class
RUN /bin/bash -c "source venv/bin/activate \
    && python -c 'from langchain_ollama import OllamaLLM; OllamaLLM(model=\"orca-mini\", temperature=0); OllamaLLM(model=\"llama3.2\", temperature=0)'"

# Make port 8000 available to the outside world
EXPOSE 8000

# Define environment variable
ENV NAME LLMChatbot

# Define the entry point for the application
CMD ["venv/bin/python", "app.py"]
