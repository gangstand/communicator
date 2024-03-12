# Stage 1: Build Stage
FROM ganggstand/python:3.12-alpine-postgresql AS build

# Installing Poetry and setting environment variables
RUN pip install poetry \
    && poetry config virtualenvs.create true \
    && poetry config virtualenvs.in-project true \
    && poetry config cache-dir /tmp/poetry_cache
ENV POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Working directory and copying dependencies
WORKDIR /app
COPY pyproject.toml ./

# Installing dependencies and clearing the cache
RUN poetry install --no-dev --no-root  \
    && poetry add uvloop httptools  \
    && rm -rf $POETRY_CACHE_DIR \
    && rm -f pyproject.toml poetry.lock

# Stage 2: Runtime Stage
FROM ganggstand/python:3.12-alpine-postgresql as runtime

# Copying the virtual environment and application
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"
COPY --from=build $VIRTUAL_ENV $VIRTUAL_ENV
COPY . .