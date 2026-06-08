# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# CSS build: bun + @tailwindcss/cli + @iconify/tailwind4 plugin
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
FROM oven/bun:1-debian AS css-build
WORKDIR /app
COPY package.json bun.lock* ./
RUN bun install --frozen-lockfile
COPY css-src ./css-src
COPY main ./main
RUN bunx tailwindcss \
        -i ./css-src/input.css \
        -o ./main/static/main/css/output.css \
        --minify


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Python build: uv + Django app
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
ARG ENVIRONMENT=local

FROM python:3.12-slim-bookworm AS py-build

ARG ENVIRONMENT

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

RUN \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --extra $ENVIRONMENT

COPY . /app

RUN uv sync --frozen --extra $ENVIRONMENT


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Runtime
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
FROM python:3.12-slim-bookworm

ARG ENVIRONMENT

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# App code + venv
COPY --from=py-build /app /app
# Built CSS
COPY --from=css-build /app/main/static/main/css/output.css /app/main/static/main/css/output.css

# Scripts
COPY ./compose/django/start /start
COPY ./compose/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /start && chmod +x /start \
    && sed -i 's/\r$//g' /entrypoint && chmod +x /entrypoint

# Non-root user
RUN addgroup --system django \
    && adduser --system --ingroup django django \
    && chown -R django:django /app /start /entrypoint

USER django

ENV ENVIRONMENT=${ENVIRONMENT}

ENTRYPOINT ["/entrypoint"]
