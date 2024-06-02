import os
from typing import Literal, List

import instructor
from groq import Groq
from ninja import NinjaAPI, Form
from pydantic import BaseModel

from functional_chatbots.prompts import SYSTEM_PROMPT, DARK_MODE_ON_INSTRUCTIONS, FULLSCREEN_MODE_ON_INSTRUCTIONS, \
    DARK_MODE_OFF_INSTRUCTIONS, FULLSCREEN_MODE_OFF_INSTRUCTIONS
from functional_chatbots.utils import render, hx_trigger_response


app = NinjaAPI()


@app.get('/')
def index(request):
    # Initialize the session state
    request.session['chat_messages'] = []
    request.session['is_dark_mode'] = False
    request.session['is_fullscreen_mode'] = False

    # Render the index template
    return render(
        request,
        'index',
        {
            'chat_messages': request.session['chat_messages'],
            'is_dark_mode': request.session['is_dark_mode'],
            'is_fullscreen_mode': request.session['is_fullscreen_mode']
        }
    )


@app.get('/chat-messages')
def list_chat_messages(request):
    # Get chat messages from session
    chat_messages = request.session.get('chat_messages', [])

    # Render the index template with the updated chat messages
    return render(request, 'index', {'chat_messages': chat_messages})


@app.post('/add-user-message')
def add_user_message(request, message: Form[str]):
    # Get chat messages from session
    chat_messages = request.session.get('chat_messages', [])

    # Add user message to session
    chat_messages.append({'role': 'user', 'content': message})

    # Trigger the `chatMessagesUpdated` client event
    return hx_trigger_response('chatMessagesUpdated')


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
                SYSTEM_PROMPT
                + (DARK_MODE_ON_INSTRUCTIONS if is_dark_mode else DARK_MODE_OFF_INSTRUCTIONS)
                + (FULLSCREEN_MODE_ON_INSTRUCTIONS if is_fullscreen_mode else FULLSCREEN_MODE_OFF_INSTRUCTIONS)
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

    # Join chatMessagesUpdated event with events from LLM response (if any)
    hx_triggers = ['chatMessagesUpdated'] + llm_response.client_events

    return hx_trigger_response(hx_triggers)


"""
Client Actions: Dark Mode and Fullscreen Mode

These endpoints toggle the session state, then render the index template with the updated toggle state.
"""


@app.post('/toggle-dark-mode')
def toggle_dark_mode(request):
    # Toggle state of `is_dark_mode`
    request.session['is_dark_mode'] = not request.session.get('is_dark_mode', False)

    # Render index with updated `is_dark_mode` state
    return render(request, 'index', {'is_dark_mode': request.session['is_dark_mode']})


@app.post('/toggle-fullscreen-mode')
def toggle_fullscreen_mode(request):
    # Toggle state of `is_fullscreen_mode`
    request.session['is_fullscreen_mode'] = not request.session.get('is_fullscreen_mode', False)

    # Render index with updated `is_fullscreen_mode` state
    return render(request, 'index', {'is_fullscreen_mode': request.session['is_fullscreen_mode']})
