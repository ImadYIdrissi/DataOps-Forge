# Use Python 3.12 slim as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency files first to leverage caching
COPY ../../../../requirements.txt ../../../../pyproject.toml /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY ../../../../ /app

# Add the working directory to PYTHONPATH
ENV PYTHONPATH="/app"

# Set an environment variable to indicate production mode
ENV PYTHONUNBUFFERED=1

# Set the default entry point to the Google Analytics pipeline
CMD ["python", "engine/data_pipelines/microservices/google_analytics_pipeline/main_pipeline.py"]
