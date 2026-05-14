from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OfflineLibraryViewSet, RegisterDownloadIntentView, SavedDownloadViewSet

router = DefaultRouter()
router.register("saved", SavedDownloadViewSet, basename="downloads-saved")
router.register("offline", OfflineLibraryViewSet, basename="downloads-offline")

urlpatterns = [
    path("", include(router.urls)),
    path("register-intent/", RegisterDownloadIntentView.as_view(), name="downloads-register-intent"),
]
