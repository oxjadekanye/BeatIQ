from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LegalSourceViewSet, MusicLicenseViewSet, TrackDownloadEligibilityView, TrackSourcesView

router = DefaultRouter()
router.register("licenses", MusicLicenseViewSet, basename="licensing-licenses")
router.register("legal-sources", LegalSourceViewSet, basename="licensing-legal-sources")

urlpatterns = [
    path("", include(router.urls)),
    path("tracks/<uuid:track_id>/sources/", TrackSourcesView.as_view(), name="licensing-track-sources"),
    path(
        "tracks/<uuid:track_id>/download-eligibility/",
        TrackDownloadEligibilityView.as_view(),
        name="licensing-track-download-eligibility",
    ),
]
