from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from am_instapound_backend.users.api.urls import urlpatterns as user_urls

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


app_name = "api"
urlpatterns = user_urls
