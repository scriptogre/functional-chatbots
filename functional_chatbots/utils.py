import json

from django.http import HttpResponse

from config.jinjax import catalog


def render(request, component_name, context=None):
    """
    Shortcut to render a JinjaX component with context. Resembles Django's `render` function.

    Notes:
        - Accepts the component's file name, without path or extension (!) (current limitation of JinjaX).
        - The component's folder must be registered in the JinjaX catalog (see `config/jinjax.py`).

    Example:
        Do this:
        >>> render(request, 'index', {...})

        And NOT this:
        >>> render(request, 'pages/index.html', {...})

    I prefer the latter option, but this is JinjaX's current approach.
    """
    if context is None:
        context = {}

    rendered_html = catalog.render(component_name, request=request, **context)

    return HttpResponse(rendered_html)


def hx_trigger_response(hx_trigger: str | list | dict):
    """
    Shortcut to return empty (204) responses with an HX-Trigger header.

    Useful for responses that only trigger client-side events in htmx.

    Accepts:
        - String for a single event without data (e.g., 'event1')
        - List of events without data (e.g., ['event1', 'event2'])
        - Dictionary with events as keys and data as values (e.g., {'event1': 'data', 'event2': None})

    Examples:
        # Trigger a single event
        >>> return hx_trigger_response('chatMessagesUpdated')

        # Trigger multiple events
        >>> return hx_trigger_response(['chatMessagesUpdated', 'pizzaOrdersUpdated'])

        # Trigger events with data
        >>> return hx_trigger_response({'pizzaOrdersUpdated': None, 'newAlert': {'message': 'A new pizza order has been placed'}})

    References:
        - HX-Trigger: https://htmx.org/headers/hx-trigger/
        - 204 Status Code: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/204
    """

    # Convert the Python structure to the correct HX-Trigger header format
    if isinstance(hx_trigger, dict):
        trigger_header = json.dumps(hx_trigger)
    elif isinstance(hx_trigger, list):
        trigger_header = ', '.join(hx_trigger)
    else:
        trigger_header = hx_trigger

    # Return a 204 response with the HX-Trigger header
    return HttpResponse(
        status=204,
        headers={'HX-Trigger': trigger_header}
    )
