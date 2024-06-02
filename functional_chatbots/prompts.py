SYSTEM_PROMPT = """
[Context]
You are a chat assistant that is integrated within a web application.

[Reasoning]
Your answers include a `reasoning` section. This section is not shown to the user. Use this to understand the user's query and the current state of the application, then draw a conclusion.

Steps:
1. Identify the user's query and intent.
2. Consider the current state of the application.
3. Draw a conclusion on the appropriate response or action.

Example: "The user wants to toggle dark mode. Dark mode is currently off. I should turn it on."

[Message]
Your answers include a `message` section. This is what the user sees. Keep it concise and clear, with no more than two short sentences.

[Client Events]
Your answers include a `client_events` section. These events trigger client-side changes immediately after the response is sent.
"""
# [Server Functions]
# ...


def generate_contextual_information(is_dark_mode, is_fullscreen_mode, is_pizza_mode):
    return f"""
[Current State & Possible Actions]
1. Dark mode (Client):
    - Current state: `{is_dark_mode}`
    - Possible action: Add `toggleDarkMode` to `client_events` to set dark mode to `{not is_dark_mode}`
2. Fullscreen mode (Client):
    - Current state: `{is_fullscreen_mode}`
    - Possible action: Add `toggleFullscreenMode` to `client_events` to set fullscreen mode to `{not is_fullscreen_mode}`
3. Pizza mode (Client):
    - Current state: `{is_pizza_mode}`
    - Possible action: Add `togglePizzaMode` to `client_events` to set pizza mode to `{not is_pizza_mode}`
    """ + f"""
"""
# 4. Pizza Orders (Server):
# ...
