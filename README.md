# Functional LLM Chatbots, DjangoCon Europe 2024

Live: **https://djangocon2024.christiantanul.com**

<img src="https://cdn.jsdelivr.net/gh/scriptogre/functional-chatbots-assets@main/0-start-here/application_final_version.gif" width="800" alt="Demo: the chatbot toggling dark mode, fullscreen, and pizza mode, then creating pizza orders." />

A demo of a Django chatbot that, in one round-trip, returns:
- a chat message,
- a list of UI events to fire (toggle dark mode, fullscreen, pizza mode),
- a list of server functions to run (CRUD on pizza orders).

Built with htmx, hyperscript, Tailwind, and a Groq-hosted Llama for inference. Originally a [DjangoCon Europe 2024 workshop](https://www.youtube.com/watch?v=0kqI_jNa2lE).

> The original workshop branches (`0-start-here` through `6-server-functions-solution`) are preserved untouched as an archive of the talk. This `main` branch is a 2026 refresh.

## Stack

- Django 5 + django-ninja 1.6 (Annotated[Form] syntax, `Status` returns)
- Jinja2 templates via django-jinja
- htmx 2 + hyperscript
- Tailwind CSS v4 (standalone CLI, no Node)
- litellm + Groq (`groq/llama-3.3-70b-versatile`)
- uv + multi-stage Dockerfile
- SQLite, in-process

## Quick start

```bash
git clone https://github.com/scriptogre/functional-chatbots
cd functional-chatbots
cp .env.example .env
# Then put your Groq API key in .env (https://console.groq.com/keys)
just
```

`just` builds Docker, runs migrations, launches the server, opens your browser, and starts Tailwind in watch mode.

## Project layout

```
config/        Django settings (split into base / local / production), URLs, WSGI/ASGI.
main/          Single Django app: NinjaAPI, LLM wrapper, templates, static assets.
main/pizza_orders/  Pizza order model, services, ninja router.
compose/       Dockerfile + start/entrypoint scripts.
docker-compose.local.yml      Hot-reload dev compose.
docker-compose.production.yml Production compose (gunicorn, no port mapping).
Justfile       Project commands (`just up`, `just makemigrations`, `just exec ...`).
```

## How it works

1. User types a message. htmx posts it to `/add-user-message`; the server appends to the session and returns a chat bubble plus `HX-Trigger: generateAssistantMessage`.
2. The trigger fires a second request to `/add-assistant-message`. The view calls `litellm.completion(...)` with Groq + JSON mode, validates the reply against a Pydantic schema, dispatches any `server_functions` (pizza CRUD), and returns the assistant bubble plus `HX-Trigger` carrying the `client_events`.
3. Each client event corresponds to a hidden htmx-armed toggle. The toggle flips, the session updates, the styling reacts via Tailwind v4 custom variants (`dark:`, `fullscreen:`, `pizza:`).

## Deploy

This repo is deployed to a homelab ThinkCentre running Docker + Caddy:

1. `docker compose -f docker-compose.production.yml up -d --build`
2. `docker network connect functional-chatbots_default caddy`
3. Add to Caddyfile:
   ```
   djangocon2024.christiantanul.com {
       import cf-tls
       reverse_proxy functional-chatbots-django-1:8000
   }
   ```
4. Reload Caddy.

## Credits

Christian Tanul. Original talk at DjangoCon Europe 2024. Refresh for 2026 keeps the demo working with current versions of every dependency.
