from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CreatorProfileDetailView, CreatorUploadBatchViewSet

router = DefaultRouter()
router.register("upload-batches", CreatorUploadBatchViewSet, basename="creators-batches")

urlpatterns = [
    path("profile/", CreatorProfileDetailView.as_view(), name="creators-profile"),
    path("", include(router.urls)),
]
