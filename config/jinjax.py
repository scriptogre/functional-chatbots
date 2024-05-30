from jinjax import Catalog

from config.settings import TEMPLATES_DIR


"""
Notes:
    - Components need to be registered to render in templates (e.g. `<ChatMessage />`)
    - Pages also need to be registered to render in views (e.g. `render(request, 'index')`)

References:
    - https://jinjax.scaletti.dev/guide/#usage
"""


# 1. Create JinjaX catalog
catalog = Catalog()

# 2. Register components
catalog.add_folder(TEMPLATES_DIR / "components")

# 3. Register layouts
catalog.add_folder(TEMPLATES_DIR / "layouts")

# 4. Register pages
catalog.add_folder(TEMPLATES_DIR / "pages")
