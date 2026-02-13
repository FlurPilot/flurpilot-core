FROM python:3.12-slim

# Install system dependencies (Geospatial libs for GeoPandas)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

WORKDIR /app

# Copy config from root context
COPY pyproject.toml poetry.lock* ./apps/worker/
COPY packages/geometry-engine/python/pyproject.toml ./packages/geometry-engine/python/ 2>/dev/null || true

# Copy poetry files to app dir
COPY apps/worker/pyproject.toml apps/worker/poetry.lock* ./apps/worker/

# Install dependencies
RUN cd apps/worker && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi || true

# Create a non-root user
RUN addgroup --system worker && adduser --system --group worker

# Copy app code and chown
COPY apps/worker ./apps/worker
RUN chown -R worker:worker /app

# Switch to non-root user
USER worker

CMD ["python", "apps/worker/main.py"]
