# Base image
FROM python:3.11-slim

# Install system dependencies for dlib
RUN apt-get update && \
    apt-get install -y build-essential cmake python3-dev libopenblas-dev liblapack-dev libjpeg-dev libpng-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Command to run on Railway
CMD ["sh", "-c", "hypercorn app:app --bind 0.0.0.0:${PORT:-8000} --reload"]