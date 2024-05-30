import os

import groq
from ninja import NinjaAPI, Form

from functional_chatbots.utils import render, hx_trigger_response


app = NinjaAPI()


@app.get('/')
def index(request):
    # 1. Initialize `chat_messages` in session
    request.session['chat_messages'] = chat_messages = []

    # 2. Render the index template
    return render(request, 'index', {'chat_messages': chat_messages})


@app.get('/chat-messages')
def list_chat_messages(request):
    """
    Notes:
        - This view is called by htmx in our #chat-messages element, upon receiving the `chatMessagesUpdated` event.
        - We use `hx-select` to select only the updated #chat-messages element from the response.
    """
    # 1. Get chat messages from session
    chat_messages = request.session.get('chat_messages', [])

    # 2. Render the index template with the updated chat messages
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

    # 3. Trigger the `chatMessagesUpdated` client event
    return hx_trigger_response('chatMessagesUpdated')


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
        """
        Notes:
            - The assistant's message should be in the format {"role": "assistant", "content": message_content}
        """

    except groq.AuthenticationError:
        chat_messages.append(
            {'role': 'assistant', 'content': "Set the GROQ_API_KEY environment variable & re-build Docker image."}
        )

    # 7. Trigger the `chatMessagesUpdated` event
    return hx_trigger_response('chatMessagesUpdated')
