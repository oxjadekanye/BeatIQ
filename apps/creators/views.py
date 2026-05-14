from rest_framework import generics, permissions, viewsets

from apps.core.drf_utils import is_schema_generation

from .models import CreatorProfile, CreatorUploadBatch
from .serializers import CreatorProfileSerializer, CreatorUploadBatchSerializer


class CreatorProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = CreatorProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        profile, _ = CreatorProfile.objects.get_or_create(
            user=self.request.user,
            defaults={"display_name": self.request.user.get_username()},
        )
        return profile


class CreatorUploadBatchViewSet(viewsets.ModelViewSet):
    serializer_class = CreatorUploadBatchSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        if is_schema_generation(self):
            return CreatorUploadBatch.objects.none()
        profile = CreatorProfile.objects.filter(user=self.request.user).first()
        if not profile:
            return CreatorUploadBatch.objects.none()
        return CreatorUploadBatch.objects.filter(creator=profile).prefetch_related("assets")

    def perform_create(self, serializer):
        profile, _ = CreatorProfile.objects.get_or_create(
            user=self.request.user,
            defaults={"display_name": self.request.user.get_username()},
        )
        serializer.save(creator=profile)
