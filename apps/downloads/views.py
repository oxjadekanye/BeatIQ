from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, inline_serializer
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.catalog.models import Track
from apps.licensing.models import LicensedTrackSource
from apps.licensing.services.download_eligibility import evaluate_download

from apps.core.drf_utils import is_schema_generation

from .models import ComplianceAuditLog, DownloadAuditLog, OfflineLibraryItem, SavedDownload
from .serializers import OfflineLibraryItemSerializer, OfflineLibraryUpsertSerializer, SavedDownloadSerializer
from .services.audit import log_compliance_event, log_download_event


class SavedDownloadViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SavedDownloadSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if is_schema_generation(self):
            return SavedDownload.objects.none()
        return (
            SavedDownload.objects.filter(user=self.request.user)
            .select_related("track", "track__primary_artist", "track__album", "licensed_track_source")
            .prefetch_related("track__genres")
        )


class OfflineLibraryViewSet(viewsets.ModelViewSet):
    serializer_class = OfflineLibraryItemSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        if is_schema_generation(self):
            return OfflineLibraryItem.objects.none()
        return (
            OfflineLibraryItem.objects.filter(user=self.request.user, removed_at__isnull=True)
            .select_related("track", "track__primary_artist", "track__album")
            .prefetch_related("track__genres")
        )

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return OfflineLibraryUpsertSerializer
        return OfflineLibraryItemSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RegisterDownloadIntentView(APIView):
    """
    Validates explicit download permission and records audit metadata.
    Actual bytes must be delivered only via partner-authorized storage flows.
    """

    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        request=inline_serializer(
            name="DownloadIntentRequest",
            fields={
                "track_id": serializers.UUIDField(),
                "licensed_track_source_id": serializers.UUIDField(),
            },
        ),
        responses={200: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT},
    )
    def post(self, request):
        track_id = request.data.get("track_id")
        lts_id = request.data.get("licensed_track_source_id")
        track = get_object_or_404(Track, pk=track_id)
        lts = get_object_or_404(LicensedTrackSource, pk=lts_id, track=track)

        log_download_event(
            user=request.user,
            track=track,
            licensed_track_source=lts,
            action=DownloadAuditLog.Action.REQUESTED,
            success=True,
            request=request,
        )

        result = evaluate_download(request.user, lts)
        if not result.allowed:
            log_download_event(
                user=request.user,
                track=track,
                licensed_track_source=lts,
                action=DownloadAuditLog.Action.DENIED,
                success=False,
                reason_code=result.reason_code,
                detail=result.detail,
                request=request,
            )
            return Response(
                {
                    "allowed": False,
                    "reason_code": result.reason_code,
                    "detail": result.detail,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        log_download_event(
            user=request.user,
            track=track,
            licensed_track_source=lts,
            action=DownloadAuditLog.Action.ALLOWED,
            success=True,
            reason_code=result.reason_code,
            detail=result.detail,
            request=request,
        )
        log_compliance_event(
            user=request.user,
            event_type=ComplianceAuditLog.EventType.STORAGE,
            payload={"kind": "download_intent_registered", "track_id": str(track.id)},
            request=request,
        )

        return Response(
            {
                "allowed": True,
                "licensed_track_source_id": result.licensed_track_source_id,
                "download_permission_id": result.permission_id,
                "next_step": "Fulfill via partner-signed URL or worker job; no stream extraction.",
            },
            status=status.HTTP_200_OK,
        )
