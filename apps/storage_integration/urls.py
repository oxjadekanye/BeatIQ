from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MyStorageObjectsViewSet

router = DefaultRouter()
router.register("objects/me", MyStorageObjectsViewSet, basename="storage-objects-me")

urlpatterns = [
    path("", include(router.urls)),
]
