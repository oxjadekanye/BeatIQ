from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, UserProfile

UserModel = get_user_model()


class BeatIQTokenObtainPairSerializer(TokenObtainPairSerializer):
    """JWT with `email_verified` claim; optional gate on unverified users."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email_verified"] = bool(user.email_verified_at)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if getattr(settings, "REQUIRE_EMAIL_VERIFICATION_FOR_JWT", False) and not user.email_verified_at:
            raise serializers.ValidationError(
                {"detail": "Email address is not verified.", "code": "email_not_verified"},
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    email_verified = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "date_joined",
            "email_verified_at",
            "email_verified",
        )
        read_only_fields = fields

    def get_email_verified(self, obj: User) -> bool:
        return obj.email_verified_at is not None


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            "user",
            "display_name",
            "avatar_url",
            "bio",
            "country_code",
            "preferences",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("user", "created_at", "updated_at")


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("display_name", "avatar_url", "bio", "country_code", "preferences")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, style={"input_type": "password"})
    password_confirm = serializers.CharField(write_only=True, min_length=8, style={"input_type": "password"})

    class Meta:
        model = UserModel
        fields = ("email", "username", "password", "password_confirm")
        extra_kwargs = {
            "username": {"required": False, "allow_blank": True},
            "email": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        attrs.pop("password_confirm", None)
        return attrs

    def validate_email(self, value: str) -> str:
        v = value.strip().lower()
        if UserModel.objects.filter(email__iexact=v).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return v

    def create(self, validated_data):
        import uuid

        password = validated_data.pop("password")
        email = validated_data["email"]
        username = (validated_data.get("username") or "").strip()
        if not username:
            base = email.split("@", 1)[0]
            username = base[:150]
        if UserModel.objects.filter(username=username).exclude(email=email).exists():
            username = f"{username[:120]}_{uuid.uuid4().hex[:8]}"
        return UserModel.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
