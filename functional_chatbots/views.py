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

    # 3. Mark the session as modified to save the changes
    request.session.modified = True

    # 4. Trigger the `chatMessagesUpdated` client event
    return hx_trigger_response('chatMessagesUpdated')
