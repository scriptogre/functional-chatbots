from django.urls import path

from app.views import api

urlpatterns = [
    path('', api.urls),
]
