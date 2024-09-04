from rest_framework.permissions import BasePermission, SAFE_METHODS


class AudioUserWritePermission(BasePermission):
    """
    Custom permission to only allow the artist that uploaded
    the audio to edit it.
    """

    message = "Editing audios is 'Restricted' to the artist only."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.artist == request.user


class IsArtistPermission(BasePermission):
    """
    Custom permission to only allow artists to add new audio.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Allow GET requests without restriction
        if request.method == "GET":
            return True

        # Check if the user is an artist for POST requests
        return request.user.is_artist
