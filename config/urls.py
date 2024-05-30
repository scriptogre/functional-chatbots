from django.urls import path

from functional_chatbots.views import app

urlpatterns = [
    path("", app.urls),
]
