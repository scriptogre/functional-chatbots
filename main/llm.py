"""LiteLLM wrapper for the assistant. Talks to Groq, returns a validated LLMResponse."""
from __future__ import annotations

import json
from typing import Literal

import litellm
from django.conf import settings
from pydantic import BaseModel, Field

from main.pizza_orders.schemas import PizzaOrderIn
from main.pizza_orders.services import (
    create_pizza_order,
    delete_pizza_order,
    update_pizza_order,
)
from main.prompts import SYSTEM_PROMPT, generate_contextual_information

MODEL = 'groq/llama-3.3-70b-versatile'

ClientEvent = Literal[
    'toggleDarkMode',
    'toggleFullscreenMode',
    'togglePizzaMode',
    'pizzaOrdersUpdated',
]
ServerFunctionName = Literal[
    'create_pizza_order',
    'update_pizza_order',
    'delete_pizza_order',
]


class ServerFunction(BaseModel):
    name: ServerFunctionName
    pizza_order_id: int | None = None
    payload: PizzaOrderIn | None = None


class LLMResponse(BaseModel):
    reasoning: str = Field(..., description='Hidden chain of thought.')
    message: str = Field(..., description='Shown to the user, one or two short sentences.')
    client_events: list[ClientEvent] = Field(default_factory=list)
    server_functions: list[ServerFunction] = Field(default_factory=list)


def generate_assistant_reply(
    chat_messages: list[dict],
    *,
    is_dark_mode: bool,
    is_fullscreen_mode: bool,
    is_pizza_mode: bool,
    pizza_orders,
) -> LLMResponse:
    """Send the conversation + state to Groq, return a validated reply."""
    system_message = {
        'role': 'system',
        'content': SYSTEM_PROMPT
        + generate_contextual_information(
            is_dark_mode, is_fullscreen_mode, is_pizza_mode, pizza_orders
        ),
    }

    response = litellm.completion(
        model=MODEL,
        api_key=settings.GROQ_API_KEY or None,
        messages=[system_message, *chat_messages],
        response_format={'type': 'json_object'},
        temperature=0.2,
    )

    content = response['choices'][0]['message']['content']
    data = json.loads(content)
    return LLMResponse.model_validate(data)


def dispatch_server_functions(functions: list[ServerFunction]) -> None:
    """Run each server function. Names match `services.py`."""
    for fn in functions:
        if fn.name == 'create_pizza_order' and fn.payload is not None:
            create_pizza_order(fn.payload)
        elif fn.name == 'update_pizza_order' and fn.pizza_order_id and fn.payload:
            update_pizza_order(fn.pizza_order_id, fn.payload)
        elif fn.name == 'delete_pizza_order' and fn.pizza_order_id:
            delete_pizza_order(fn.pizza_order_id)
