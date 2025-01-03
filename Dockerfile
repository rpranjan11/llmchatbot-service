# Stage 1: Python application setup
FROM python:3.11-slim

# Define build arguments
ARG OPENAPI_API_KEY
ARG OPENAPI_ASSISTANT_ID
ARG MIDDLEWARE_ALLOW_ORIGIN_URL

# Set environment variables
ENV OPENAPI_API_KEY=${OPENAPI_API_KEY}
ENV OPENAPI_ASSISTANT_ID=${OPENAPI_ASSISTANT_ID}
ENV MIDDLEWARE_ALLOW_ORIGIN_URL=${MIDDLEWARE_ALLOW_ORIGIN_URL}

# Log the build arguments (for debugging purposes)
RUN echo "OpenAPI API Key: $OPENAPI_API_KEY" && \
    echo "OpenAPI Assistant ID: $OPENAPI_ASSISTANT_ID" && \
    echo "Middleware Origin URL: $MIDDLEWARE_ALLOW_ORIGIN_URL"

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Create a virtual environment and install dependencies
RUN python -m venv venv && \
    venv/bin/pip install --no-cache-dir -r requirements.txt

# Preload the models using the `OllamaLLM` class
RUN venv/bin/python -c \
    "from langchain_ollama import OllamaLLM; \
    OllamaLLM(model='orca-mini', temperature=0); \
    OllamaLLM(model='llama3.2', temperature=0)" || echo "Model preloading failed, continuing..."

# Install Nginx
RUN apt-get update && apt-get install -y nginx

# Create nginx user
RUN adduser --system --no-create-home --disabled-login --disabled-password --group nginx

# Copy Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf
COPY llmchatbot-service.conf /etc/nginx/conf.d/llmchatbot-service.conf

# Copy SSL certificates
COPY server.crt /etc/nginx/ssl/server.crt
COPY server.key /etc/nginx/ssl/server.key

# Expose ports for HTTP and HTTPS
EXPOSE 80 8930

# Start Nginx and the application
CMD ["sh", "-c", "nginx -g 'daemon off;' & venv/bin/python app.py"]