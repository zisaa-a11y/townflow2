from rest_framework import permissions


class IsFileOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only file owners to edit or delete their files.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            # Allow if file is public or user is the owner
            return obj.is_public or obj.uploaded_by == request.user

        # Write permissions are only allowed to the owner
        return obj.uploaded_by == request.user


class IsFileOwner(permissions.BasePermission):
    """
    Custom permission to allow only file owners to access their files.
    """

    def has_object_permission(self, request, view, obj):
        return obj.uploaded_by == request.user
