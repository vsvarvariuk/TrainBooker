from rest_framework import permissions


class IsAdminOrIsAuthenticatedReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True

        if request.user and request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True

        return False
