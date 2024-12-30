# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the Ollama package
RUN pip install ollama

# Pull the orca-mini
RUN ollama pull orca-mini

# Pull the llama3.2
RUN ollama pull llama3.2

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download the orca-mini and llama3.2 models using the updated class
RUN python -c "from langchain_ollama import OllamaLLM; OllamaLLM(model='orca-mini', temperature=0); OllamaLLM(model='llama3.2', temperature=0)"

# Make port 80 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME LLMChatbot

# Run app.py when the container launches
CMD ["python", "app.py"]