from rest_framework.permissions import BasePermission

from common.constants.enums import UserRole


class IsAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in {UserRole.ADMIN, UserRole.MODERATOR}
        )


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user
            and request.user.is_authenticated
            and (obj.user_id == request.user.id or request.user.role == UserRole.ADMIN)
        )
