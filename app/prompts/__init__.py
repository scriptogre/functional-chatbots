"""LLM prompt templates. Usage: prompts.render('system.jinja', **ctx)."""
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


class PromptEnvironment(Environment):
    def render(self, name: str, **kwargs) -> str:
        return self.get_template(name).render(**kwargs).strip()


prompts = PromptEnvironment(
    loader=FileSystemLoader(Path(__file__).parent),
    keep_trailing_newline=False,
    trim_blocks=True,
    lstrip_blocks=True,
)
