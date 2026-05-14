from rest_framework import permissions, viewsets

from apps.core.drf_utils import is_schema_generation

from .models import AIMoodDiscoverySession, AIRecognitionPrepJob
from .serializers import AIMoodDiscoverySessionSerializer, AIRecognitionPrepJobSerializer


class AIMoodDiscoverySessionViewSet(viewsets.ModelViewSet):
    serializer_class = AIMoodDiscoverySessionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        if is_schema_generation(self):
            return AIMoodDiscoverySession.objects.none()
        return AIMoodDiscoverySession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        from apps.ai_services.services.mood_discovery import enqueue_mood_discovery

        session = serializer.save(user=self.request.user)
        enqueue_mood_discovery(session)


class AIRecognitionPrepJobViewSet(viewsets.ModelViewSet):
    serializer_class = AIRecognitionPrepJobSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        if is_schema_generation(self):
            return AIRecognitionPrepJob.objects.none()
        return AIRecognitionPrepJob.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        from apps.ai_services.services.recognition_prep import enqueue_recognition_prep

        job = serializer.save(user=self.request.user)
        enqueue_recognition_prep(job)
