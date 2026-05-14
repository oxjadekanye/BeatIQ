from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AIPlaylistRecommendationViewSet, PlaylistViewSet

router = DefaultRouter()
router.register("lists", PlaylistViewSet, basename="playlist-lists")
router.register(
    "ai/recommendations",
    AIPlaylistRecommendationViewSet,
    basename="playlist-ai-recommendations",
)

urlpatterns = [
    path("", include(router.urls)),
]
