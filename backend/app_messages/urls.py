from rest_framework.routers import DefaultRouter

from app_messages.views import MessagesViewSet

router = DefaultRouter()

router.register("messages", MessagesViewSet, basename="messages")
