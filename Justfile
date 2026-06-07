# Default: run app
default: run

# Start app (compose + browser + tailwind watch)
run *args: tailwindcss-setup-cli
    #!/usr/bin/env sh
    trap 'kill 0' EXIT
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

# Tailwind CLI setup (downloads matching binary if missing)
tailwindcss-setup-cli:
    #!/usr/bin/env bash
    if [ -f "./tailwindcss" ] || [ -f "./tailwindcss.exe" ]; then
        echo "Tailwind CSS CLI already installed."
        exit 0
    fi
    TAILWIND_VERSION="v4.3.0"
    BASE_URL="https://github.com/tailwindlabs/tailwindcss/releases/download/${TAILWIND_VERSION}"
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    ARCH=$(uname -m)
    case "$OS-$ARCH" in
        darwin-arm64) BINARY="tailwindcss-macos-arm64" ;;
        darwin-x86_64) BINARY="tailwindcss-macos-x64" ;;
        linux-x86_64) BINARY="tailwindcss-linux-x64" ;;
        linux-aarch64) BINARY="tailwindcss-linux-arm64" ;;
        *) echo "Unsupported $OS-$ARCH. Edit Justfile."; exit 1 ;;
    esac
    echo "Downloading $BINARY..."
    curl -sL -o ./tailwindcss "$BASE_URL/$BINARY"
    chmod +x ./tailwindcss

# Tailwind watch + minify
tailwindcss-watch:
    ./tailwindcss -i ./css-src/input.css -o ./main/static/main/css/output.css --watch --minify

# Tailwind one-shot build
tailwindcss-build:
    ./tailwindcss -i ./css-src/input.css -o ./main/static/main/css/output.css --minify
