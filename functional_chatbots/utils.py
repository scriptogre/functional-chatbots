from django.http import HttpResponse

from config.jinjax import catalog


def render(request, component_name, context=None, headers=None):
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

    return HttpResponse(rendered_html, headers=headers)
