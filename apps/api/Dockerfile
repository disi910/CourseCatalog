# Python FastAPI backend for CourseCatalog
# Uses python:3.12-slim (Debian-based, ~150MB, smaller than full python:3.12)

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies needed by psycopg2 (PostgreSQL driver)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (Python dependency manager, like npm for Python)
RUN pip install poetry

# Copy dependency files first (Docker caches this layer)
# If dependencies haven't changed, Docker skips the install on rebuild
COPY pyproject.toml poetry.lock ./

# Install dependencies into the system Python (not a virtualenv)
# --no-root: don't install our project as a package yet
# --no-interaction: don't ask questions
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction

# Now copy the actual source code
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Run the FastAPI server
# --host 0.0.0.0 makes it accessible from other containers (not just localhost)
# --port 8000 is where nginx expects to find the API
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
