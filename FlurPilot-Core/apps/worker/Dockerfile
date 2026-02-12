FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (Geospatial libs for GeoPandas)
# Security Hardening: --no-install-recommends to keep image small
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy config
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Create a non-root user
RUN addgroup --system worker && adduser --system --group worker

# Copy app code and chown
COPY . .
RUN chown -R worker:worker /app

# Switch to non-root user
USER worker

CMD ["python", "main.py"]
