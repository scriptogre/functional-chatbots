# Default: run app
default: run

# Start app (compose + browser + tailwind watch)
run *args:
    #!/usr/bin/env sh
    trap 'kill 0' EXIT
    bun install --frozen-lockfile
    just up {{ args }} &
    (sleep 4 && uv run -m webbrowser http://localhost:8000) &
    just tailwindcss-watch
    wait

# Bring up local containers
up *args:
    docker compose -f docker-compose.local.yml up {{ args }}

# Tear down + wipe volumes
destroy:
    docker compose -f docker-compose.local.yml down --volumes

# Run any command in the django container
exec +cmd:
    docker compose -f docker-compose.local.yml run --rm django {{ cmd }}

# Make migrations
makemigrations *args:
    docker compose -f docker-compose.local.yml run --rm django python manage.py makemigrations {{ args }}

# Apply migrations
migrate:
    docker compose -f docker-compose.local.yml run --rm django python manage.py migrate

# Tailwind watch + minify (uses bunx so @iconify/tailwind4 plugin loads)
tailwindcss-watch:
    bunx tailwindcss -i ./css-src/input.css -o ./main/static/main/css/output.css --watch --minify

# Tailwind one-shot build
tailwindcss-build:
    bun install --frozen-lockfile
    bunx tailwindcss -i ./css-src/input.css -o ./main/static/main/css/output.css --minify
