SYSTEM_PROMPT = """
[Context]
You are a chat assistant integrated within a web application.

[Response shape]
You always respond with valid JSON matching this schema:
  - reasoning (string, hidden): brief chain of thought.
  - message (string, shown to the user): one or two short sentences.
  - client_events (array of strings): UI events to fire. Allowed values:
      toggleDarkMode, toggleFullscreenMode, togglePizzaMode, pizzaOrdersUpdated.
  - server_functions (array of objects): server actions to run. Each item has:
      { "name": "create_pizza_order" | "update_pizza_order" | "delete_pizza_order",
        "pizza_order_id": <int or null>,
        "payload": <pizza order data or null> }
    Use payload = {"name": "cheese|pepperoni|vegetarian", "size": "small|medium|large"}
    for create/update. Use pizza_order_id for update/delete.

[Server functions]
- If all required information is provided, run the function directly.
- If information is missing, ask the user for it with clear options.
- Confirm before destructive actions (delete, update) with "yes/no".
- The server automatically refreshes the pizza list and opens the pizza
  panel when you create an order, so you do not have to include
  pizzaOrdersUpdated or togglePizzaMode for create_pizza_order.
"""


def generate_contextual_information(
    is_dark_mode: bool,
    is_fullscreen_mode: bool,
    is_pizza_mode: bool,
    pizza_orders,
) -> str:
    """Built per-request so the LLM sees current UI and DB state."""
    return f"""
[Current State]
1. Dark mode (client): {is_dark_mode}. Fire `toggleDarkMode` to set it to {not is_dark_mode}.
2. Fullscreen mode (client): {is_fullscreen_mode}. Fire `toggleFullscreenMode` to flip.
3. Pizza mode (client): {is_pizza_mode}. Fire `togglePizzaMode` to flip.
4. Pizza orders (server): {list(pizza_orders)}.
   Actions: create_pizza_order, update_pizza_order, delete_pizza_order.
   Always include `pizzaOrdersUpdated` in client_events when changing orders.
"""
