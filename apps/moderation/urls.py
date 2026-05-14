from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FileModerationReportView, ModerationStaffQueueViewSet

router = DefaultRouter()
router.register("queue", ModerationStaffQueueViewSet, basename="moderation-queue")

urlpatterns = [
    path("reports/", FileModerationReportView.as_view(), name="moderation-file-report"),
    path("", include(router.urls)),
]
