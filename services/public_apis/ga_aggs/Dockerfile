# Stage 1: Build the `engine` package
ARG PYTHON_BASE_VERSION=3.12
FROM python:${PYTHON_BASE_VERSION}-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the `engine` source code
COPY engine /build/engine

# Create a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Build the wheel with a custom output directory using `python -m build`
RUN pip install --no-cache-dir build && \
    cd engine && \
    python -m build --wheel --outdir /build/output

# Stage 2: Build the application image
FROM python:${PYTHON_BASE_VERSION}-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install the `engine` wheel from the builder stage
COPY --from=builder /build/output/*.whl /app/
RUN pip install --no-cache-dir /app/*.whl

# Copy application-specific requirements
COPY services/public_apis/ga_aggs/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the service code
COPY services/public_apis/ga_aggs /app/

# Expose the port and set the default entry point
EXPOSE 8080
CMD ["python", "main.py"]
