from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

import am_instapound_backend.pictures.api.views as api_views

router: SimpleRouter

# pylint: disable=duplicate-code
if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()
# pylint: enable=duplicate-code

router.register("pictures", api_views.PictureViewSet)
router.register("picture-comments", api_views.PictureCommentViewSet)

urlpatterns = router.urls
