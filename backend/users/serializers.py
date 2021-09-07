from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    class Meta:
        model = User
        fields = ("email", "username", "id")


class RegisterSerializer(serializers.ModelSerializer):
    """Registration serializer."""

    password1 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": _("Password")},
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": _("Repeat password")},
    )

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")

    def validate(self, data):
        """Validate password."""
        password1 = data["password1"]
        password2 = data["password2"]
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError(_("The two passwords do not match."))
        return data

    def create(self, validated_data):
        """Create user."""
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            is_active=True,
            is_staff=False,
        )
        user.set_password(validated_data["password1"])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    """Login serializer."""

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        max_length=128,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ("email", "password")

    def validate(self, data):
        username = data.get("email")
        password = data.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        data["user"] = user
        return data
