from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    """

    def has_permission(self, request, view):
        # Check if the request is a read-only request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check if the user is an admin
        return request.user and request.user.is_staff