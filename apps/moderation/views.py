from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ModerationReport
from .serializers import ModerationReportCreateSerializer, ModerationReportSerializer


class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class FileModerationReportView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        request=ModerationReportCreateSerializer,
        responses={201: ModerationReportSerializer},
    )
    def post(self, request):
        ser = ModerationReportCreateSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        report = ser.save()
        return Response(ModerationReportSerializer(report).data, status=status.HTTP_201_CREATED)


class ModerationReportStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModerationReport
        fields = ("status",)


class ModerationStaffQueueViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ModerationReport.objects.select_related("reporter").prefetch_related("actions")
    permission_classes = (IsStaffUser,)
    http_method_names = ["get", "patch", "head", "options"]

    def get_serializer_class(self):
        if self.action in ("update", "partial_update"):
            return ModerationReportStatusSerializer
        return ModerationReportSerializer
