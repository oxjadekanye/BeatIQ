from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SocialLinkMetadataViewSet

router = DefaultRouter()
router.register("links", SocialLinkMetadataViewSet, basename="social-links")

urlpatterns = [
    path("", include(router.urls)),
]
