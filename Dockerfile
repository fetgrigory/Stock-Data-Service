# Basic Python image
FROM python:3.12.6-bookworm

# Environment configuration for Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Working directory in the container
WORKDIR /app

# Install uv package manager for dependency management
RUN pip install --no-cache-dir uv

# Copy dependency metadata and install locked dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# Copy application source code
COPY . .

# Launching FastAPI via uvicorn
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]