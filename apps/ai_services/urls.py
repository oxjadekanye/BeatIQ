from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AIMoodDiscoverySessionViewSet, AIRecognitionPrepJobViewSet

router = DefaultRouter()
router.register("mood-sessions", AIMoodDiscoverySessionViewSet, basename="ai-mood")
router.register("recognition-prep", AIRecognitionPrepJobViewSet, basename="ai-recognition-prep")

urlpatterns = [
    path("", include(router.urls)),
]
