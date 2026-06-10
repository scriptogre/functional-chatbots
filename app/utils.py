"""Render helper: Jinja2 template -> HttpResponse with optional headers."""
from __future__ import annotations

from django.http import HttpResponse
from django.template.loader import render_to_string


def render(request, name: str, context: dict | None = None, headers: dict | None = None) -> HttpResponse:
    """Render a Jinja2 template by name (without `.jinja`) and wrap in HttpResponse.

    Example: render(request, 'index', {...})
    """
    template_name = name if name.endswith('.jinja') else f'{name}.jinja'
    html = render_to_string(template_name, context or {}, request=request)
    return HttpResponse(html, headers=headers)
