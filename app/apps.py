from django.apps import AppConfig


class AppConfig_(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    label = 'main'

    def ready(self):
        """Warm the chat loop at boot so the first request doesn't pay the
        openai SDK import cost."""
        from app import services  # noqa: F401
