FROM nvidia/cuda:12.6.0-cudnn-runtime-ubuntu24.04

WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-venv python3-pip pipx \
    build-essential python3-dev \
    cmake pkg-config \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:${PATH}"

RUN pipx install poetry==2.0.1

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

COPY pyproject.toml poetry.lock /app/

# Poetry config
ENV POETRY_HTTP_TIMEOUT=600
ENV POETRY_HTTP_RETRIES=10
ENV PIP_DEFAULT_TIMEOUT=600
ENV PIP_RETRIES=10
RUN poetry config installer.max-workers 1

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=cache,target=/root/.cache/pypoetry \
    poetry install --no-interaction --no-ansi

COPY . .
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:${PATH}"

RUN chmod +x ./scripts/backend-dev-start.sh
CMD ["bash", "./scripts/backend-dev-start.sh"]