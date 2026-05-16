# ImaraFund Production Dockerfile - Python 3.12 (All Issues Fixed)
FROM python:3.12-slim

WORKDIR /app

# Environment optimization
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for grant file uploads
RUN mkdir -p /app/uploads && chmod 755 /app/uploads

# Security: non-root user
RUN useradd -m -u 1000 imarafund && \
    chown -R imarafund:imarafund /app
USER imarafund

# Expose Cloud Run port
EXPOSE 8080

# Start application (NO HEALTHCHECK - this was causing deployment failures)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
