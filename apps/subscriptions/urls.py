from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MySubscriptionViewSet, PlanViewSet

router = DefaultRouter()
router.register("plans", PlanViewSet, basename="subscription-plans")
router.register("me", MySubscriptionViewSet, basename="subscription-me")

urlpatterns = [
    path("", include(router.urls)),
]
