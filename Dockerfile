# syntax=docker/dockerfile:1

# Use official slim Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies if needed (optional: build tools, curl, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements and install all Python packages
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Optional: install your local package in editable mode if you have pyproject.toml
# COPY pyproject.toml . 
# COPY orbisage_router ./orbisage_router
# RUN pip install -e .

# Copy the rest of the project code into the image
COPY . .

# Make sure your code is importable
ENV PYTHONPATH=/app

# Expose port for web
EXPOSE 7860

# Default command to run the Streamlit or Gradio app
CMD ["python", "web/app.py"]
