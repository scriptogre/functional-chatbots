import os
from typing import Literal, List

import instructor
from groq import Groq
from ninja import NinjaAPI, Form
from pydantic import BaseModel

from functional_chatbots.prompts import CONTEXT_AND_RULES, REASONING_INSTRUCTIONS, create_client_events_instructions
from functional_chatbots.utils import render


app = NinjaAPI()


@app.get('/')
def index(request):
    # Initialize the session state
    request.session['chat_messages'] = chat_messages = []
    request.session['is_dark_mode'] = is_dark_mode = False
    request.session['is_fullscreen_mode'] = is_fullscreen_mode = False

    # Render the index template
    return render(
        request,
        'index',
        {
            'chat_messages': chat_messages,
            'is_dark_mode': is_dark_mode,
            'is_fullscreen_mode': is_fullscreen_mode
        }
    )


@app.post('/add-user-message')
def add_user_message(request, message: Form[str]):
    # Get chat messages from session
    chat_messages = request.session.get('chat_messages', [])

    # Add user message to session
    chat_messages.append({'role': 'user', 'content': message})

    # Trigger the `addAssistantMessage` client event
    return render(
        request,
        'ChatMessage',
        context={'role': 'user', '__content': message},
        headers={'HX-Trigger': 'addAssistantMessage'}
    )


@app.post('/add-assistant-message')
def add_assistant_message(request):
    # Initialize Groq client
    llm_70b = Groq(api_key=os.environ.get('GROQ_API_KEY'))

    # Apply instructor to LLM client
    structured_llm_70b = instructor.from_groq(llm_70b, mode=instructor.Mode.JSON)

    # Get state of dark & fullscreen mode
    is_dark_mode = request.session.get('is_dark_mode', False)
    is_fullscreen_mode = request.session.get('is_fullscreen_mode', False)

    # Add instructions based on these states
    system_message = {
        "role": "system",
        "content": (
                CONTEXT_AND_RULES
                + REASONING_INSTRUCTIONS
                # Add client events instructions based on current state
                + create_client_events_instructions(is_dark_mode, is_fullscreen_mode)
        )
    }

    # Get chat messages
    chat_messages = request.session.get('chat_messages', [])

    # Define LLM response schema
    class LLMResponse(BaseModel):
        reasoning: str
        client_events: List[Literal["toggleDarkMode", "toggleFullscreenMode"]] = []
        message: str

    # Generate LLM response with defined schema
    llm_response = structured_llm_70b.chat.completions.create(
        model="llama3-70b-8192",
        messages=[system_message] + chat_messages,
        response_model=LLMResponse
    )

    # Add assistant message to session
    chat_messages.append({'role': 'assistant', 'content': llm_response.json()})

    return render(
        request,
        'ChatMessage',
        context={'role': 'assistant', '__content': llm_response.message},
        headers={'HX-Trigger': ', '.join(llm_response.client_events)}
    )


"""
Dark & Fullscreen Mode

These endpoints toggle the session state, then render the index template with the updated toggle state.
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
