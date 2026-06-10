"""LLM chat loop. Registers tools, calls Groq, returns text + UI events."""
import json

from django.conf import settings
from openai import OpenAI

from app.pizza_orders.services import (
    create_pizza_order,
    delete_pizza_order,
    update_pizza_order,
)
from app.prompts import prompts
from app.tools import TOOL_DEFINITIONS, TOOLS, register

# Pizza CRUD is owned by pizza_orders/; registered here so that module stays
# LLM-agnostic.
for func in (create_pizza_order, update_pizza_order, delete_pizza_order):
    register(func)


@register
def toggle_dark_mode():       """Flip the dark-mode UI state."""

@register
def toggle_fullscreen_mode(): """Flip the fullscreen UI state."""

@register
def toggle_pizza_mode():      """Flip the pizza panel visibility."""


CLIENT_EVENTS = {
    'toggle_dark_mode': 'toggleDarkMode',
    'toggle_fullscreen_mode': 'toggleFullscreenMode',
    'toggle_pizza_mode': 'togglePizzaMode',
}
PIZZA_TOOLS = {'create_pizza_order', 'update_pizza_order', 'delete_pizza_order'}

client = OpenAI(api_key=settings.GROQ_API_KEY, base_url='https://api.groq.com/openai/v1')


def generate_assistant_message(
    chat_messages,
    *,
    session_key,
    is_dark_mode,
    is_fullscreen_mode,
    is_pizza_mode,
    pizza_orders,
):
    """Run the chat loop. Returns (text, events). Calls the LLM; if it asks
    for tools, runs them, renders each result via prompts/tools/<name>.jinja,
    feeds the results back, and repeats until the LLM returns text."""
    messages = [
        {'role': 'system', 'content': prompts.render(
            'system.jinja',
            is_dark_mode=is_dark_mode,
            is_fullscreen_mode=is_fullscreen_mode,
            is_pizza_mode=is_pizza_mode,
            pizza_orders=pizza_orders,
        )},
        *chat_messages,
    ]
    events: list[str] = []

    for _ in range(3):
        msg = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=messages,
            temperature=0.2,
            tools=TOOL_DEFINITIONS,
        ).choices[0].message

        if not msg.tool_calls:
            return (msg.content or 'Done.').strip(), events

        messages.append(msg.model_dump(exclude_none=True))
        for call in msg.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments or '{}')

            if name in CLIENT_EVENTS:
                event = CLIENT_EVENTS[name]
                if event not in events:
                    events.append(event)
                result = None
            else:
                result = TOOLS[name](**args, session_key=session_key)
                if name in PIZZA_TOOLS and 'pizzaOrdersUpdated' not in events:
                    events.append('pizzaOrdersUpdated')
                if name == 'create_pizza_order' and not is_pizza_mode and 'togglePizzaMode' not in events:
                    events.append('togglePizzaMode')

            messages.append({
                'role': 'tool',
                'tool_call_id': call.id,
                'content': prompts.render(f'tools/{name}.jinja', result=result),
            })

    return 'Done.', events
