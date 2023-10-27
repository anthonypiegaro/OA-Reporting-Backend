from rest_framework import permissions

class IsStaffOrSelf(permissions.BasePermission):
    """
    Custom permission:
    - Allow full access for staff users
    - Allow access to indivudual user detail view for the user themselves
    - Deny access otherwise
    """

    def has_permission(self, request, view):
        # Allow access to list view and other views for staff users
        if request.user.is_staff:
            return True

        # For non-staff users, only allow access to detail views
        return view.action in ['retrieve', 'update', 'partial_update', 'destroy']

    def has_object_permission(self, request, view, obj):
        # Allow access to the user's own record, deny access otherwise
        return request.user.is_staff or obj == request.user
