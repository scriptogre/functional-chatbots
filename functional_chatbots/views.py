import os
from typing import Literal, List

import instructor
from groq import Groq
from ninja import NinjaAPI, Form
from pydantic import BaseModel

from functional_chatbots.pizza_orders.models import PizzaOrder
from functional_chatbots.prompts import SYSTEM_PROMPT, generate_contextual_information
from functional_chatbots.utils import render
from functional_chatbots.pizza_orders.views import router as pizza_orders_router

app = NinjaAPI()
app.add_router('', pizza_orders_router)


@app.get('/')
def index(request):
    # Start fresh on page load
    request.session['chat_messages'] = chat_messages = []
    request.session['is_dark_mode'] = is_dark_mode = False
    request.session['is_fullscreen_mode'] = is_fullscreen_mode = False
    request.session['is_pizza_mode'] = is_pizza_mode = False
    PizzaOrder.objects.all().delete()

    # Render the index template
    return render(
        request,
        'index',
        {
            'chat_messages': chat_messages,
            'is_dark_mode': is_dark_mode,
            'is_fullscreen_mode': is_fullscreen_mode,
            'is_pizza_mode': is_pizza_mode,
            'pizza_orders': []
        }
    )


@app.post('/add-user-message')
def add_user_message(request, message: Form[str]):
    # Get chat messages from session
    chat_messages = request.session.get('chat_messages', [])

    # Add user message to session
    chat_messages.append({'role': 'user', 'content': message})

    # Return the response
    return render(
        request,
        'ChatMessage',
        context={'role': 'user', '__content': message},
        headers={'HX-Trigger': 'generateAssistantMessage'}
    )


@app.post('/add-assistant-message')
def add_assistant_message(request):
    # Initialize Groq client
    llm_70b = Groq(api_key=os.environ.get('GROQ_API_KEY'))

    # Apply instructor to LLM client
    structured_llm_70b = instructor.from_groq(llm_70b, mode=instructor.Mode.JSON)

    # Get client state (dark & fullscreen mode), and server state (pizza orders)
    is_dark_mode = request.session.get('is_dark_mode', False)
    is_fullscreen_mode = request.session.get('is_fullscreen_mode', False)
    is_pizza_mode = request.session.get('is_pizza_mode', False)

    # Add instructions based on these states
    system_message = {
        "role": "system",
        "content": SYSTEM_PROMPT + generate_contextual_information(is_dark_mode, is_fullscreen_mode, is_pizza_mode)
    }

    # Get chat messages
    chat_messages = request.session.get('chat_messages', [])

    # Define LLM response schema
    class LLMResponse(BaseModel):
        reasoning: str
        # TODO: server_functions: ...
        client_events: List[Literal["toggleDarkMode", "toggleFullscreenMode", "togglePizzaMode", "pizzaOrdersUpdated"]] = []
        message: str

    # Generate LLM response with defined schema
    llm_response = structured_llm_70b.chat.completions.create(
        model="llama3-70b-8192", messages=[system_message] + chat_messages, response_model=LLMResponse
    )

    # Add assistant message to session
    chat_messages.append({'role': 'assistant', 'content': llm_response.json()})

    # Handle the actual calling of the functions
    # ...

    return render(
        request,
        'ChatMessage',
        {'role': 'assistant', '__content': llm_response.message},
        {'HX-Trigger': ', '.join(llm_response.client_events)}
    )


"""
Dark Mode and Fullscreen Mode
"""


@app.post('/toggle-dark-mode')
def toggle_dark_mode(request):
    # Toggle state of `is_dark_mode`
    request.session['is_dark_mode'] = is_dark_mode = not request.session.get('is_dark_mode', False)

    # Render index with updated `is_dark_mode` state
    return render(request, 'index', {'is_dark_mode': is_dark_mode})


@app.post('/toggle-fullscreen-mode')
def toggle_fullscreen_mode(request):
    # Toggle state of `is_fullscreen_mode`
    request.session['is_fullscreen_mode'] = is_fullscreen_mode = not request.session.get('is_fullscreen_mode', False)

    # Render index with updated `is_fullscreen_mode` state
    return render(request, 'index', {'is_fullscreen_mode': is_fullscreen_mode})


@app.post('/toggle-pizza-mode')
def toggle_pizza_mode(request):
    # Toggle state of `is_pizza_mode`
    request.session['is_pizza_mode'] = is_pizza_mode = not request.session.get('is_pizza_mode', False)

    # Render index with updated `is_pizza_mode` state
    return render(request, 'index', {'is_pizza_mode': is_pizza_mode})
