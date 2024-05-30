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

    # 3. Mark the session as modified to save the changes
    request.session.modified = True

    # 4. Render the HTML of a <ChatMessage/> component
    # Note: `__content` is a special prop for a component's `{{ content }}`
    return render(
        request,
        'ChatMessage',
        context={'role': 'user', '__content': message},
        # TODO: Include an HX-Trigger response header that says `addAssistantMessage`
        # References:
        #   - HX-Trigger Response Header: https://htmx.org/headers/hx-trigger/
        #   - hx-trigger attribute: https://htmx.org/attributes/hx-trigger/
        headers={}
    )


@app.post('/add-assistant-message')
def add_assistant_message(request):
    """
    TODO: Implement the add_assistant_message view function
    """
    # 1. Initialize the Groq client
    # llm_70b = ...
    """
    Notes:
        - Set the `api_key` parameter to the value of GROQ_API_KEY env variable.
        - You can use os.getenv() for this.
    """

    # 2. Get chat messages from session
    # chat_messages = ...

    # 3. Create a system message in the format {"role": "system", "content": "system_prompt_here"}
    # system_message = ...

    # 4. Get the completion using llm_70b.chat.completions.create method
    # completion = ...
    """
    Notes:
        - Set the `model` parameter to "llama3-70b-8192"
        - The `messages` parameter expects a list in the format [{"role": "user", "content": "message"}, ...]
        - Set `messages` parameter to a concatenation of system_message and chat_messages, with system_message first.
    """

    # 5. Extract the message content from the completion. It is found in completion.choices[0].message.content
    # message_content = ...

    # 6. Append assistant's message content to the chat messages list
    # chat_messages.append(...)
    """
    Notes:
        - The assistant's message should be in the format {"role": "assistant", "content": message_content}
    """

    # 7. Mark the session as modified to save the changes
    # request.session.modified = True

    # 8. Render the HTML of a <ChatMessage/> component with the assistant's message
