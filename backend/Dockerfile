# syntax=docker.io/docker/dockerfile:1

# Define version variables similar style to frontend
ARG PYTHON_IMAGE=python:3.13-slim

FROM ${PYTHON_IMAGE} AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project metadata first for better caching
COPY pyproject.toml uv.lock ./

# Install runtime dependencies using pip from pyproject
# We install the project in editable mode later for dev override; for production we install the built package.
# First install build backend so pip can build the project defined by pyproject.toml
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir hatchling \
    && pip wheel --no-cache-dir --wheel-dir /wheels . || true

# Copy the rest of the application code
COPY . .

# Install the package (this will install runtime deps declared in pyproject)
RUN pip install --no-cache-dir .

# Create a non-root user similar to frontend image practice
RUN useradd --create-home --uid 1001 appuser && mkdir -p /app/logs && chown -R appuser:appuser /app/logs
USER appuser

EXPOSE 8000

# Default command: run uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
