# Get environment as build arg (defaults to local)
ARG ENVIRONMENT=local

FROM python:3.12-slim-bookworm AS builder

ARG ENVIRONMENT

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies (cached)
RUN \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --extra $ENVIRONMENT

COPY . /app

# Install project
RUN uv sync --frozen --extra $ENVIRONMENT


# Final stage
FROM python:3.12-slim-bookworm

ARG ENVIRONMENT
ARG TAILWIND_VERSION=v4.3.0

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PATH="/app/.venv/bin:$PATH"

# Install curl for Tailwind CLI download
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy app and venv
COPY --from=builder /app /app

# Scripts
COPY ./compose/django/start /start
COPY ./compose/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /start && chmod +x /start \
    && sed -i 's/\r$//g' /entrypoint && chmod +x /entrypoint

# Download Tailwind v4 standalone CLI for linux-x64
RUN curl -sL -o /usr/local/bin/tailwindcss \
        "https://github.com/tailwindlabs/tailwindcss/releases/download/${TAILWIND_VERSION}/tailwindcss-linux-x64" \
    && chmod +x /usr/local/bin/tailwindcss

# Build CSS once (production); local mounts the source over this anyway
RUN mkdir -p ./main/static/main/css && tailwindcss \
        -i ./css-src/input.css \
        -o ./main/static/main/css/output.css \
        --minify

# Non-root user
RUN addgroup --system django \
    && adduser --system --ingroup django django \
    && chown -R django:django /app /start /entrypoint

USER django

ENV ENVIRONMENT=${ENVIRONMENT}

ENTRYPOINT ["/entrypoint"]
