from rest_framework import mixins, permissions, viewsets

from apps.core.drf_utils import is_schema_generation

from .models import Plan, Subscription
from .serializers import PlanSerializer, SubscriptionSerializer


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plan.objects.filter(is_public=True)
    serializer_class = PlanSerializer
    permission_classes = (permissions.AllowAny,)


class MySubscriptionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if is_schema_generation(self):
            return Subscription.objects.none()
        return Subscription.objects.filter(user=self.request.user).select_related("plan")
