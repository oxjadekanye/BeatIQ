from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from apps.accounts.views import BeatIQTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("auth/token/", BeatIQTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("accounts/", include("apps.accounts.urls")),
    path("catalog/", include("apps.catalog.urls")),
    path("licensing/", include("apps.licensing.urls")),
    path("downloads/", include("apps.downloads.urls")),
    path("playlists/", include("apps.playlists.urls")),
    path("ai/", include("apps.ai_services.urls")),
    path("social/", include("apps.social_metadata.urls")),
    path("creators/", include("apps.creators.urls")),
    path("subscriptions/", include("apps.subscriptions.urls")),
    path("storage/", include("apps.storage_integration.urls")),
    path("moderation/", include("apps.moderation.urls")),
]
