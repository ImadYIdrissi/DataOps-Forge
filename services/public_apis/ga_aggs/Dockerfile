# Use Python 3.12 slim as the base image
# TODO : Interpolate PYTHON_VERSION from global .env
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Set debconf to noninteractive mode to prevent debconf from attempting interactive conf
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies for building Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    apt-utils gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python -m venv /opt/venv

# Ensure the virtual environment is used by default
ENV PATH="/opt/venv/bin:$PATH"

# Copy service-specific requirements
COPY requirements.txt /app/

# Install dependencies inside the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the service code into the container
COPY . /app

# Add the working directory to PYTHONPATH
ENV PYTHONPATH="/app"

# Expose the port for Cloud Run
EXPOSE 8080

# Set an environment variable to indicate production mode
ENV PYTHONUNBUFFERED=1

# Set the default entry point to the FastAPI app
CMD ["python", "main.py"]
