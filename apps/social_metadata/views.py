from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.drf_utils import is_schema_generation

from .models import SocialLinkMetadata
from .serializers import SocialLinkMetadataSerializer, SocialLinkResolveRequestSerializer
from .services.link_detection import resolve_share_url


class SocialLinkMetadataViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SocialLinkMetadataSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if is_schema_generation(self):
            return SocialLinkMetadata.objects.none()
        return SocialLinkMetadata.objects.filter(submitted_by=self.request.user).select_related(
            "resolved_track",
            "resolved_track__primary_artist",
            "resolved_track__album",
        )

    @action(detail=False, methods=["post"], url_path="resolve")
    def resolve(self, request):
        ser = SocialLinkResolveRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        url = ser.validated_data["url"]
        meta = resolve_share_url(url, user=request.user)
        return Response(SocialLinkMetadataSerializer(meta).data, status=status.HTTP_201_CREATED)
