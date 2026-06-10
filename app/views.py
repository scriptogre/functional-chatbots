"""NinjaAPI with chat + toggles, plus the pizza orders router."""
import logging
from typing import Annotated

from django.http import HttpResponse
from ninja import Form, NinjaAPI

logger = logging.getLogger(__name__)

from app.pizza_orders.services import (
    delete_all_pizza_orders,
    list_pizza_orders,
)
from app.pizza_orders.views import router as pizza_orders_router
from app.services import generate_assistant_message
from app.utils import render

api = NinjaAPI()
api.add_router('', pizza_orders_router)


def _ensure_session_key(request) -> str:
    """Force Django to create a session key on first hit so we can scope
    pizza orders to this browser."""
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key


@api.get('/')
def index(request):
    """Restore this session's state. Survives reloads. POST /reset wipes it."""
    session_key = _ensure_session_key(request)
    return render(request, 'index', {
        'chat_messages': request.session.setdefault('chat_messages', []),
        'is_dark_mode': request.session.setdefault('is_dark_mode', False),
        'is_fullscreen_mode': request.session.setdefault('is_fullscreen_mode', False),
        'is_pizza_mode': request.session.setdefault('is_pizza_mode', False),
        'pizza_orders': list(list_pizza_orders(session_key)),
    })


@api.post('/reset')
def reset(request):
    """Wipe chat history, UI flags, and this session's pizza orders."""
    session_key = _ensure_session_key(request)
    delete_all_pizza_orders(session_key)
    for key in ('chat_messages', 'is_dark_mode', 'is_fullscreen_mode', 'is_pizza_mode'):
        request.session.pop(key, None)
    return HttpResponse(status=204, headers={'HX-Refresh': 'true'})


@api.post('/add-user-message')
def add_user_message(request, message: Annotated[str, Form()]):
    chat_messages = request.session.get('chat_messages', [])
    chat_messages.append({'role': 'user', 'content': message})
    request.session['chat_messages'] = chat_messages
    return render(
        request,
        'partials/chat_message',
        {'role': 'user', 'content': message},
        headers={'HX-Trigger': 'generateAssistantMessage'},
    )


@api.post('/add-assistant-message')
def add_assistant_message(request):
    """Generate the assistant's next message. Tool calls (pizza CRUD,
    UI toggles) run inside the chat loop; the returned events become
    HX-Trigger headers so htmx flips toggles + refreshes the pizza panel."""
    from openai import APIError, RateLimitError

    session_key = _ensure_session_key(request)
    chat_messages = request.session.get('chat_messages', [])

    try:
        text, events = generate_assistant_message(
            chat_messages,
            session_key=session_key,
            is_dark_mode=request.headers.get('X-Dark-Mode') == 'true',
            is_fullscreen_mode=request.session.get('is_fullscreen_mode', False),
            is_pizza_mode=request.session.get('is_pizza_mode', False),
            pizza_orders=[
                {'id': o.id, 'name': o.name, 'size': o.size,
                 'seconds_left': o.seconds_left, 'is_finished': o.is_finished}
                for o in list_pizza_orders(session_key)
            ],
        )
    except RateLimitError:
        text, events = (
            "The assistant is over its free-tier limit for now. Try again in a few minutes.",
            [],
        )
    except APIError:
        logger.exception('LLM call failed')
        text, events = (
            "The assistant is having trouble right now. Please try again.",
            [],
        )
    else:
        chat_messages.append({'role': 'assistant', 'content': text})
        request.session['chat_messages'] = chat_messages

    headers = {'HX-Trigger': ', '.join(events)} if events else None
    return render(
        request,
        'partials/chat_message',
        {'role': 'assistant', 'content': text},
        headers=headers,
    )


@api.post('/toggle-dark-mode')
def toggle_dark_mode(request):
    """Flip based on actual client state (via X-Dark-Mode header), not
    session. Keeps the server in sync when OS-pref seeded dark before any
    server-side click happened."""
    current = request.headers.get('X-Dark-Mode') == 'true'
    request.session['is_dark_mode'] = is_dark_mode = not current
    return render(request, 'index', {'is_dark_mode': is_dark_mode})


@api.post('/toggle-fullscreen-mode')
def toggle_fullscreen_mode(request):
    request.session['is_fullscreen_mode'] = is_fullscreen_mode = not request.session.get(
        'is_fullscreen_mode', False
    )
    return render(request, 'index', {'is_fullscreen_mode': is_fullscreen_mode})


@api.post('/toggle-pizza-mode')
def toggle_pizza_mode(request):
    request.session['is_pizza_mode'] = is_pizza_mode = not request.session.get(
        'is_pizza_mode', False
    )
    return render(request, 'index', {'is_pizza_mode': is_pizza_mode})
