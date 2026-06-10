"""LLM tool registration. No domain knowledge here."""
import inspect
from typing import Callable

from pydantic import create_model

TOOLS: dict[str, Callable] = {}
TOOL_DEFINITIONS: list[dict] = []


def register(func: Callable) -> Callable:
    """Register a function as an LLM tool. Type hints + docstring become
    the JSON schema. Keyword-only params with defaults are server-injected
    and excluded from the schema."""
    TOOLS[func.__name__] = func
    TOOL_DEFINITIONS.append({'type': 'function', 'function': {
        'name': func.__name__,
        'description': (func.__doc__ or '').strip(),
        'parameters': _schema(func),
    }})
    return func


def _schema(func: Callable) -> dict:
    fields = {
        n: (p.annotation, ... if p.default is inspect.Parameter.empty else p.default)
        for n, p in inspect.signature(func).parameters.items()
        if not (p.kind is inspect.Parameter.KEYWORD_ONLY and p.default is not inspect.Parameter.empty)
    }
    out = (
        create_model(func.__name__, **fields).model_json_schema()
        if fields else {'type': 'object', 'properties': {}}
    )
    out.pop('title', None)
    return out
