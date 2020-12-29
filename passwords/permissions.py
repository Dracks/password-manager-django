from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and (
                request.method in SAFE_METHODS or request.user.is_staff
            )
        )
