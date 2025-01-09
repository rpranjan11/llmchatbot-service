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

# Expose ports for HTTP and HTTPS
EXPOSE 80 443

# Start Nginx and the application
CMD ["sh", "-c", "nginx -g 'daemon off;' & venv/bin/python app.py"]