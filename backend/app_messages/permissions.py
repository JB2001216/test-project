from rest_framework import permissions


class IsOwnerOnly(permissions.BasePermission):
    """
    Permissions if owner only.
    """

    def has_object_permission(self, request, view, obj):
        if request.user == obj.from_user:
            return True
        return False
