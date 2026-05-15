from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, UserProfile
from .services.account_activation import normalize_email

UserModel = get_user_model()


class BeatIQTokenObtainPairSerializer(TokenObtainPairSerializer):
    """JWT with `email_verified` claim; case-insensitive email login with clear errors."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email_verified"] = bool(user.email_verified_at)
        return token

    def validate(self, attrs):
        email = normalize_email(attrs.get(self.username_field) or "")
        password = attrs.get("password") or ""
        if not email or not password:
            raise serializers.ValidationError(
                {"detail": "Email and password are required.", "code": "credentials_required"},
            )

        user = UserModel.objects.filter(email__iexact=email).first()
        if user is None:
            raise serializers.ValidationError(
                {
                    "detail": "No BeatIQ account exists for this email. Create an account first.",
                    "code": "account_not_found",
                },
            )
        if not user.is_active:
            raise serializers.ValidationError(
                {
                    "detail": "This account is not active yet. Verify your email or contact support.",
                    "code": "account_inactive",
                },
            )
        if not user.check_password(password):
            raise serializers.ValidationError(
                {"detail": "Incorrect password.", "code": "invalid_password"},
            )
        if getattr(settings, "REQUIRE_EMAIL_VERIFICATION_FOR_JWT", False) and not user.email_verified_at:
            raise serializers.ValidationError(
                {
                    "detail": "Email address is not verified. Check your inbox for the verification link.",
                    "code": "email_not_verified",
                },
            )

        self.user = user
        refresh = self.get_token(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


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
            "birth_year",
            "birth_month",
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
    password = serializers.CharField(write_only=True, min_length=6, style={"input_type": "password"})
    password_confirm = serializers.CharField(write_only=True, min_length=6, style={"input_type": "password"})
    full_name = serializers.CharField(write_only=True, max_length=255)
    birth_year = serializers.IntegerField(write_only=True, min_value=1900, max_value=2100)
    birth_month = serializers.IntegerField(write_only=True, min_value=1, max_value=12)

    class Meta:
        model = UserModel
        fields = (
            "email",
            "username",
            "password",
            "password_confirm",
            "full_name",
            "birth_year",
            "birth_month",
        )
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

        full_name = (validated_data.pop("full_name", "") or "").strip()
        birth_year = validated_data.pop("birth_year", None)
        birth_month = validated_data.pop("birth_month", None)
        password = validated_data.pop("password")
        email = validated_data["email"]
        username = (validated_data.get("username") or "").strip()
        if not username:
            base = email.split("@", 1)[0]
            username = base[:150]
        if UserModel.objects.filter(username=username).exclude(email=email).exists():
            username = f"{username[:120]}_{uuid.uuid4().hex[:8]}"
        first_name = ""
        last_name = ""
        if full_name:
            parts = full_name.split(None, 1)
            first_name = parts[0][:150]
            last_name = (parts[1] if len(parts) > 1 else "")[:150]
        user = UserModel.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
        )
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.display_name = full_name or profile.display_name
        profile.birth_year = birth_year
        profile.birth_month = birth_month
        profile.save()
        return user
