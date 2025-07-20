# Use Python base image (amd64)
FROM --platform=linux/amd64 python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app/ ./app/

# Set entry point
CMD ["python", "app/main.py"]
