# This Dockerfile is intended solely for local development of Misago
# If you are seeking a suitable Docker setup for running Misago in a 
# production, please use misago-docker instead
FROM ghcr.io/astral-sh/uv:python3.12-bookworm

ENV IN_MISAGO_DOCKER=1
ENV MISAGO_PLUGINS="/app/plugins"

# Enable uv's bytecode compilation for better performance
ENV UV_COMPILE_BYTECODE=1
# Copy dependencies from the uv-managed venv into the container
# rather than symlinking (helps if using ephemeral volumes)
ENV UV_LINK_MODE=copy

# Disable buffering for Python
ENV PYTHONUNBUFFERED=1


# Install env dependencies in one single command/layer
RUN apt-get update && apt-get install -y \
    vim \
    libffi-dev \
    libssl-dev \
    sqlite3 \
    libjpeg-dev \
    libopenjp2-7-dev \
    locales \
    cron \
    postgresql-client-15 \
    gettext

# Add files and dirs for build step
# ADD dev /app/dev

ADD plugins /app/plugins

WORKDIR /app/

# --- 2) Prepare the Python environment with uv ---
# Copy in just uv.lock and pyproject.toml for caching the dependency layer
COPY uv.lock pyproject.toml /app/

# Let uv build your venv and install dependencies (frozen, no dev deps)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

COPY . .

RUN uv run manage.py collectstatic --noinput

EXPOSE 8000
