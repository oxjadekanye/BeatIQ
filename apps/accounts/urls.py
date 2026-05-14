from django.urls import path

from .views import (
    MeView,
    RegisterView,
    ResendVerificationView,
    UserProfileDetailView,
    VerifyEmailView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="accounts-register"),
    path("verify-email/", VerifyEmailView.as_view(), name="accounts-verify-email"),
    path("resend-verification/", ResendVerificationView.as_view(), name="accounts-resend-verification"),
    path("me/", MeView.as_view(), name="accounts-me"),
    path("profile/", UserProfileDetailView.as_view(), name="accounts-profile"),
]
