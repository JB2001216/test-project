import json

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from app_messages.models import Message
from app_messages.permissions import IsOwnerOnly
from app_messages.serializers import (
    MessagesSerializer,
    MessagesInboxSerializer,
    MessagesOutboxSerializer,
    MessagesCreateSerializer
)

User = get_user_model()


class MessagesViewSet(ModelViewSet):
    """Users messages."""

    serializer_class = MessagesSerializer
    queryset = Message.objects.all()
    http_method_names = ("get", "post", "delete")
    permission_classes = [
        IsAuthenticated,
    ]
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [permission() for permission in (IsOwnerOnly,)]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """Create message or save errors."""
        data = request.data.copy()
        to_user_email = request.data.pop("to_user")
        user = get_object_or_404(User, email=to_user_email)
        data["to_user"] = user.id
        serializer = MessagesCreateSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def list(self, request, *args, **kwargs):
        """Only messages from the recipient or sender."""
        self.queryset = Message.objects.filter(
            Q(from_user=request.user) | Q(to_user=request.user)
        )
        return super().list(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["GET"],
        url_name="inbox",
        http_method_names=("get",),
        pagination_class=LimitOffsetPagination,
        serializer_class=MessagesInboxSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def inbox(self, request):
        """User inbox messages."""
        messages = Message.objects.filter(to_user=request.user)
        page = self.paginate_queryset(messages.all())
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer( messages.all(), many=True)
        return Response(serializer.data)


    @action(
        detail=False,
        methods=["GET"],
        url_name="outbox",
        http_method_names=("get",),
        serializer_class=MessagesOutboxSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def outbox(self, request):
        """User outbox messages."""
        messages = Message.objects.filter(from_user=request.user)
        page = self.paginate_queryset(messages.all())
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(messages.all(), many=True)
        return Response(serializer.data)

