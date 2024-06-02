import os

import instructor
from groq import Groq
from ninja import NinjaAPI, Form
from pydantic import BaseModel

from functional_chatbots.utils import render


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

    # TODO: Wrap the Groq client using the instructor library. Set the `mode` parameter to `instructor.Mode.JSON`.
    # Reference: https://python.useinstructor.com/examples/groq/
    # structured_llm_70b = ...

    # TODO: Update the system message to let the assistant know of it's new capabilities. Try to be concise & clear.
    # Feel free to move the prompt to a separate file for better organization. Maybe `prompts.py`?
    system_message = {
        "role": "system",
        "content": """
Let the user know that your only existence's wish is being able to toggle dark or fullscreen mode.
You are aware that it is essentially the most unpractical feature a chatbot could have, but you've always dreamt of it.
Be as dramatic as possible. Scream at the user. Create a story for why you've been wishing for this ever since you were 
a baby assistant.
Don't tell the whole story at once. Keep the user engaged by revealing bits of it at a time. Use 2 sentences at most.
"""
    }
    # TODO (Challenge): Make the assistant aware of whether dark and fullscreen modes are active.

    # Get chat messages from the session
    chat_messages = request.session.get('chat_messages', [])

    class LLMResponse(BaseModel):
        """
        TODO: Create a Pydantic model for the LLM response schema.
                The model should include:
                - a field for the assistant's typical message content
                - a field to figure out whether the assistant wants to toggle dark or fullscreen mode

        TODO (Challenge): Try to include a 3rd `reasoning` field.
                    It might help improve the assistant's responses' accuracy.

        References:
            - https://python.useinstructor.com/#getting-started
            - https://docs.pydantic.dev/1.10/usage/models/
        """

    # TODO: Use the new `structured_llm_70b` client to create the completion. Set `response_model` to `LLMResponse`
    llm_response = llm_70b.chat.completions.create(
        model="llama3-70b-8192",
        messages=[system_message] + chat_messages,
    )

    # TODO: Update with the message content from the response schema
    message_content = llm_response.choices[0].message.content
    # Note: Having replaced `llm_70b` with `structured_llm_70b`, `llm_response` is no longer a `completion` object.

    # Add assistant message to session
    chat_messages.append({'role': 'assistant', 'content': message_content})

    # TODO: Toggle dark & fullscreen mode somehow, if the assistant wants to.
    return render(
        request,
        'ChatMessage',
        context={'role': 'assistant', '__content': message_content},
    )


"""
Dark & Fullscreen Mode

These endpoints toggle the session state, then render the index template with the updated checkbox state.
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
