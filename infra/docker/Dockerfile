# syntax=docker/dockerfile:1.7
FROM python:3.12.3-slim

WORKDIR /opt/app
ENV POETRY_VERSION=1.8.2 \
    POETRY_HOME=/opt/poetry \
    PATH="/opt/poetry/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Install system deps & Poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential git \
    && pip install "poetry==$POETRY_VERSION" \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* ./ 
COPY app ./app
RUN poetry install --no-dev --only main

# Entrypoint (agent cron runner by default)
CMD ["python", "-m", "app.job_search_llm_agent.agent"]
