import os

import groq
from ninja import NinjaAPI, Form

from functional_chatbots.utils import render


app = NinjaAPI()


@app.get('/')
def index(request):
    # 1. Initialize `chat_messages` in session
    request.session['chat_messages'] = chat_messages = []

    # 2. Render the index template
    return render(request, 'index', {'chat_messages': chat_messages})


@app.post('/add-user-message')
def add_user_message(request, message: Form[str]):
    """
    Notes:
        - We can parse request.POST data directly from our view function parameters, saving some boilerplate.

    References:
        - https://django-ninja.dev/guides/input/form-params/
    """
    # 1. Get chat messages from session
    chat_messages = request.session.get('chat_messages', [])

    # 2. Add user message to session
    chat_messages.append({'role': 'user', 'content': message})

    # Note: `__content` is a special prop for a component's `{{ content }}`
    return render(
        request,
        'ChatMessage',
        context={'role': 'user', '__content': message},
        headers={'HX-Trigger': 'addAssistantMessage'}
    )


@app.post('/add-assistant-message')
def add_assistant_message(request):
    # 1. Initialize the Groq client
    llm_70b = groq.Groq(api_key=os.environ.get('GROQ_API_KEY'))

    # 2. Get chat messages from session
    chat_messages = request.session.get('chat_messages', [])

    # 3. Create a system message
    system_message = {
        "role": "system",
        "content": "Respond with a witty & amusing haiku roasting the user for not changing the system prompt."
                   "Encourage the user to update it."
    }

    try:
        # 4. Get the LLM completion
        completion = llm_70b.chat.completions.create(
            model="llama3-70b-8192",
            messages=[system_message] + chat_messages
        )

        # 5. Extract the message content from the completion
        message_content = completion.choices[0].message.content

        # 6. Append assistant's message content to the chat messages list
        chat_messages.append({"role": "assistant", "content": message_content})

    except groq.AuthenticationError:
        message_content = "Set the GROQ_API_KEY environment variable & re-build Docker image."
        chat_messages.append(
            {'role': 'assistant', 'content': message_content}
        )

    return render(
        request,
        'ChatMessage',
        context={'role': 'assistant', '__content': message_content},
    )
