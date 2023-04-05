from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Access level - only for admin
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin


class AdminOrReadOnly(permissions.BasePermission):
    """
    Get method is available for all users,
    PATCH, DELETE - only for administrator
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method in (
            'PATCH',
            'POST',
            'DELETE',
        ):
            return request.user.is_admin
        return request.method == 'GET'


class IsUserWithPowerOrReadOnly(permissions.BasePermission):
    """
    Get method is available for all users,
    POST, PATCH, DELETE - only for author, admin or moderator
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
