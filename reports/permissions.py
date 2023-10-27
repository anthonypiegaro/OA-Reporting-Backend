from rest_framework import permissions

class CustomPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow any read-only requests
        return request.user.is_staff  # Only allow writes for staff users
