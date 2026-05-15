from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserProfile
from .serializers import (
    BeatIQTokenObtainPairSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
    UserSerializer,
)
from .services.email_verification import build_verification_token, parse_verification_token
from .tasks import (
    enqueue_or_apply_sync,
    notify_admin_new_signup_task,
    send_verification_email_task,
    send_welcome_email_task,
)

User = get_user_model()


class MeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(responses={200: UserProfileSerializer})
    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        return Response(UserProfileSerializer(profile).data)


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return UserProfileUpdateSerializer
        return UserProfileSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = "register"

    @extend_schema(
        request=RegisterSerializer,
        responses={201: OpenApiTypes.OBJECT},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        enqueue_or_apply_sync(notify_admin_new_signup_task, args=(str(user.pk),))
        token = build_verification_token(str(user.pk))
        path = reverse("accounts-verify-email")
        verify_url = request.build_absolute_uri(path) + "?" + urlencode({"token": token})
        enqueue_or_apply_sync(send_verification_email_task, args=(str(user.pk), verify_url))
        headers = self.get_success_headers({})
        return Response(
            {
                "user": UserSerializer(user).data,
                "detail": "Verification email sent. Check your inbox to activate your account.",
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class VerifyEmailView(APIView):
    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        parameters=[
            OpenApiParameter("token", OpenApiTypes.STR, OpenApiParameter.QUERY, required=True),
        ],
        responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        token = request.query_params.get("token")
        if not token:
            return Response({"detail": "Missing token.", "code": "token_required"}, status=status.HTTP_400_BAD_REQUEST)
        max_age = getattr(settings, "EMAIL_VERIFICATION_TOKEN_MAX_AGE_SECONDS", 3 * 24 * 3600)
        user_id = parse_verification_token(token, max_age_seconds=max_age)
        if not user_id:
            return Response(
                {"detail": "Invalid or expired verification link.", "code": "token_invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found.", "code": "user_not_found"}, status=status.HTTP_404_NOT_FOUND)

        if user.email_verified_at:
            return Response({"detail": "Email already verified.", "user": UserSerializer(user).data})

        user.email_verified_at = timezone.now()
        user.save(update_fields=["email_verified_at"])
        enqueue_or_apply_sync(send_welcome_email_task, args=(str(user.pk),))
        return Response(
            {
                "detail": "Email verified successfully.",
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class ResendVerificationView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        request=None,
        responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT},
    )
    def post(self, request):
        user = request.user
        if user.email_verified_at:
            return Response(
                {"detail": "Email is already verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = build_verification_token(str(user.pk))
        path = reverse("accounts-verify-email")
        verify_url = request.build_absolute_uri(path) + "?" + urlencode({"token": token})
        enqueue_or_apply_sync(send_verification_email_task, args=(str(user.pk), verify_url))
        return Response({"detail": "Verification email sent."}, status=status.HTTP_200_OK)


@extend_schema(
    request=BeatIQTokenObtainPairSerializer,
    responses={200: OpenApiTypes.OBJECT},
)
class BeatIQTokenObtainPairView(TokenObtainPairView):
    serializer_class = BeatIQTokenObtainPairSerializer
