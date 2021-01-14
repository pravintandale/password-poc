from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    """
    User Permissions:
    User should be authenticated for all actions except create.
    User not allowed to delete its object.
    """

    def has_permission(self, request, view):
        if (request.user.is_authenticated and view.action != 'destroy') or view.action == 'create':
            return True
        return False
