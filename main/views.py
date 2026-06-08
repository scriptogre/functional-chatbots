"""NinjaAPI with chat + toggles, plus the pizza orders router."""
from typing import Annotated

from ninja import Form, NinjaAPI

from main.llm import dispatch_server_functions, generate_assistant_reply
from main.pizza_orders.models import PizzaOrder
from main.pizza_orders.services import list_pizza_orders
from main.pizza_orders.views import router as pizza_orders_router
from main.utils import render

api = NinjaAPI()
api.add_router('', pizza_orders_router)


@api.get('/')
def index(request):
    """Fresh state on every page load (it's a demo, not a real app)."""
    request.session['chat_messages'] = chat_messages = []
    request.session['is_dark_mode'] = is_dark_mode = False
    request.session['is_fullscreen_mode'] = is_fullscreen_mode = False
    request.session['is_pizza_mode'] = is_pizza_mode = False
    PizzaOrder.objects.all().delete()

    return render(
        request,
        'index',
        {
            'chat_messages': chat_messages,
            'is_dark_mode': is_dark_mode,
            'is_fullscreen_mode': is_fullscreen_mode,
            'is_pizza_mode': is_pizza_mode,
            'pizza_orders': [],
        },
    )


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
    is_dark_mode = request.session.get('is_dark_mode', False)
    is_fullscreen_mode = request.session.get('is_fullscreen_mode', False)
    is_pizza_mode = request.session.get('is_pizza_mode', False)
    pizza_orders = list(PizzaOrder.objects.all().values('id', 'name', 'size'))
    chat_messages = request.session.get('chat_messages', [])

    reply = generate_assistant_reply(
        chat_messages,
        is_dark_mode=is_dark_mode,
        is_fullscreen_mode=is_fullscreen_mode,
        is_pizza_mode=is_pizza_mode,
        pizza_orders=pizza_orders,
    )

    chat_messages.append({'role': 'assistant', 'content': reply.model_dump_json()})
    request.session['chat_messages'] = chat_messages

    dispatch_server_functions(reply.server_functions)

    client_events = list(reply.client_events)
    pizza_changed = any(
        fn.name.endswith('pizza_order') for fn in reply.server_functions
    )
    if pizza_changed and 'pizzaOrdersUpdated' not in client_events:
        client_events.append('pizzaOrdersUpdated')

    # Auto-show the pizza panel when an order is created and pizza mode is off,
    # otherwise the user can't see the order they just placed.
    created_order = any(fn.name == 'create_pizza_order' for fn in reply.server_functions)
    if created_order and not is_pizza_mode and 'togglePizzaMode' not in client_events:
        client_events.append('togglePizzaMode')

    return render(
        request,
        'partials/chat_message',
        {'role': 'assistant', 'content': reply.message},
        headers={'HX-Trigger': ', '.join(client_events)} if client_events else None,
    )


@api.post('/toggle-dark-mode')
def toggle_dark_mode(request):
    request.session['is_dark_mode'] = is_dark_mode = not request.session.get('is_dark_mode', False)
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
