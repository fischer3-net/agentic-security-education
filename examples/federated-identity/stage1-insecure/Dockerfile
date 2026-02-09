# Stage 1 - Insecure Federated Identity Implementation
# Dockerfile for running demonstrations

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default command (can be overridden)
CMD ["python", "naive_agents.py"]

# Labels
LABEL maintainer="security-education@example.com"
LABEL description="Stage 1: Insecure Federated Identity (Educational)"
LABEL version="1.0"
LABEL security.warning="INTENTIONALLY INSECURE - DO NOT USE IN PRODUCTION"
