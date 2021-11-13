from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

import am_instapound_backend.users.api.views as api_views

router: SimpleRouter

# pylint: disable=duplicate-code
if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()
# pylint: enable=duplicate-code

# router.register("users", <FILLME>)

urlpatterns = [
                  path('users/register/', api_views.RegistrationView.as_view(), name='register'),
              ] + router.urls
