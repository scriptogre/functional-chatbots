from django.urls import path

from main.views import api

urlpatterns = [
    path('', api.urls),
]
