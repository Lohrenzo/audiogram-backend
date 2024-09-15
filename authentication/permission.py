from rest_framework.permissions import BasePermission, SAFE_METHODS


class UpdateUserPermission(BasePermission):
    """
    Custom permission to only allow the current user that uploaded
    the album to edit it.
    """

    message = "Editing user details is 'Restricted' to the user only."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.artist == request.user
