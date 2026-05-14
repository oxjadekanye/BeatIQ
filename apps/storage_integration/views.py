from rest_framework import mixins, permissions, viewsets

from apps.core.drf_utils import is_schema_generation

from .models import ManagedStorageObject
from .serializers import ManagedStorageObjectSerializer


class MyStorageObjectsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Lists storage objects owned by the user (signed URL generation happens in a service layer)."""

    serializer_class = ManagedStorageObjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if is_schema_generation(self):
            return ManagedStorageObject.objects.none()
        return ManagedStorageObject.objects.filter(owner=self.request.user).select_related("provider")
