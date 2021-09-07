from django.contrib.auth import get_user_model
from rest_framework import serializers

from app_messages.models import Message

User = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):
    """Username, id, email"""

    class Meta:
        model = User
        fields = ("username", "email", "id")


class MessagesSerializer(serializers.ModelSerializer):
    """User serializer."""

    class Meta:
        model = Message
        fields = ("from_user", "to_user", "text", "title", "id", "created")


class MessagesInboxSerializer(serializers.ModelSerializer):
    """Inbox serializer."""

    from_user = SimpleUserSerializer()
    to_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = ("from_user", "to_user", "text", "title", "id", "created")


class MessagesOutboxSerializer(serializers.ModelSerializer):
    """Outbox serializer."""

    to_user = SimpleUserSerializer()
    from_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = ("from_user", "to_user", "text", "title", "id", "created")


class MessagesCreateSerializer(serializers.ModelSerializer):
    """Create message serializer."""

    from_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = ("from_user", "to_user", "title", "text", "id")

