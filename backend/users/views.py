from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserSerializer, LoginSerializer, RegisterSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    """User view."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ("get",)
    permission_classes = [
        AllowAny,
    ]
    pagination_class = LimitOffsetPagination

    @action(
        detail=False,
        methods=["POST"],
        url_name="login",
        http_method_names=("post",),
        serializer_class=LoginSerializer,
        permission_classes=(AllowAny,),
    )
    def login(self, request):
        """Login for users."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        response_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response(status=status.HTTP_200_OK, data=response_data)

    @action(
        detail=False,
        methods=["POST"],
        url_name="registration",
        http_method_names=("post",),
        serializer_class=RegisterSerializer,
        permission_classes=(AllowAny,),
    )
    def register(self, request):
        """Registration for users."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response_data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response(status=status.HTTP_200_OK, data=response_data)

    @action(
        detail=False,
        methods=["GET"],
        url_name="me",
        http_method_names=("get",),
        serializer_class=UserSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        """Authenticated users info."""
        serializer = self.serializer_class(instance=request.user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
