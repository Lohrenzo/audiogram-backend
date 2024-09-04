import os

import jwt

# from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics, status  # viewsets,
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import JSONParser, MultiPartParser  # FormParser,
from rest_framework.permissions import (
    # DjangoModelPermissions,
    # DjangoModelPermissionsOrAnonReadOnly,
    IsAdminUser,
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response

from .models import Album, Audio, Genre, Playlist
from .permission import AudioUserWritePermission, IsArtistPermission
from .serializers import (
    AlbumSerializer,
    AudioSerializer,
    GenreSerializer,
    PlaylistSerializer,
)

# from rest_framework.views import APIView


class AudioView(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser]
    permission_classes = [
        IsAuthenticated,
        IsArtistPermission,
        # AllowAny,
    ]
    queryset = Audio.released_audios.all()
    serializer_class = AudioSerializer
    # ordering_fields = [
    #     "artist",
    #     "producer",
    #     "album",
    #     "genre",
    # ]
    filterset_fields = [
        "artist",
        "producer",
        "album",
        "genre",
    ]
    search_fields = [
        "title",
        "genre__title",
    ]
    # The double underscore helps with searching in a nested field like genre.

    def get_queryset(self):
        return Audio.released_audios.all()
        # return Audio.objects.filter(likes=self.request.user)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def post(self, request, format=None):
        print(request.data)
        serializer = AudioSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )
        if serializer.is_valid():
            audio = serializer.save()
            return Response(
                f"Audio '{audio.title}' has been added.",
                status=status.HTTP_200_OK,
                content_type="text/plain",
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserAudiosView(generics.ListAPIView):
    """
    View to return the audios created by the current user.
    """

    serializer_class = AudioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the albums
        that were created by the currently authenticated user.
        """
        return Audio.objects.filter(artist=self.request.user)

    def list(self, request, *args, **kwargs):
        """
        Override the list method to customize the response.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            content_type="application/json",
        )


@api_view(["POST"])
def increment_play_count(request, audio_id):
    try:
        audio = Audio.objects.get(id=audio_id)
        audio.increment_play_count()
        return Response({"status": "success", "play_count": audio.play_count})
    except Audio.DoesNotExist:
        return Response(
            {"status": "error", "message": "Audio not found"},
            status=404,
        )


class AudioDetail(
    generics.RetrieveUpdateDestroyAPIView,
    AudioUserWritePermission,
):
    permission_classes = [AudioUserWritePermission]
    parser_classes = [MultiPartParser]
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer


class LikesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AudioSerializer
    # parser_classes = [MultiPartParser]

    def get_queryset(self):
        return Audio.objects.filter(likes=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            content_type="application/json",
        )

    def create(self, request, *args, **kwargs):
        audio_id = request.data.get("audioId")
        audio = get_object_or_404(Audio, id=audio_id)
        if audio.likes.filter(id=request.user.id).exists():
            return Response(
                {"detail": "This audio is already liked by the user."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        audio.likes.add(request.user)
        serializer = self.get_serializer(audio)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GenreView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    parser_classes = [JSONParser]
    serializer_class = GenreSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        - For 'POST' requests: Only admins can create new genres.
        - For 'GET' requests: Only authenticated users can view genres.
        """
        if self.request.method == "POST":
            permission_classes = [IsAdminUser]
        elif self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def post(self, request):
        print(request.data)
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            genre = serializer.save()
            return Response(
                f"Genre '{genre.title}' has been added.",
                status=status.HTTP_200_OK,
                content_type="text/plain",
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class AlbumView(generics.ListCreateAPIView):
    # permission_classes = [AllowAny]
    queryset = Album.objects.all()
    parser_classes = [MultiPartParser]
    serializer_class = AlbumSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        - For 'POST' requests: Only artists can create new albums.
        - For 'GET' requests: Only authenticated users can view albums.
        """
        if self.request.method == "POST":
            permission_classes = [IsArtistPermission]
        elif self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def post(self, request):
        print(request.data)
        serializer = AlbumSerializer(
            data=request.data,
            context={
                "request": request
            },  # Pass the request object to the serializer context
        )
        if serializer.is_valid():
            album = serializer.save()
            return Response(
                f"Album '{album.title}' has been added.",
                status=status.HTTP_200_OK,
                content_type="text/plain",
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserAlbumsView(generics.ListAPIView):
    """
    View to return the albums created by the current user.
    """

    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the albums
        that were created by the currently authenticated user.
        """
        return Album.objects.filter(artist=self.request.user)

    def list(self, request, *args, **kwargs):
        """
        Override the list method to customize the response.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            content_type="application/json",
        )


class PlaylistView(generics.ListCreateAPIView):
    # Define the queryset and serializers
    queryset = Playlist.objects.all()
    parser_classes = [MultiPartParser, JSONParser]
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]

    # Override the post method to handle the creation of a new playlist
    def post(self, request):
        print(request.data)
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            playlist = serializer.save()
            return Response(
                f"Playlist '{playlist.title}' created.",
                status=status.HTTP_200_OK,
                content_type="text/plain",
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Override the get_queryset method to filter by user_id if provided
    def get_queryset(self):
        queryset = Playlist.objects.all()
        # Get the user_id from query parameters
        user_id = self.request.query_params.get("user_id", None)

        # Extract JWT token from the Authorization header
        token = self.request.headers.get("Authorization", None)
        if token is None:
            raise AuthenticationFailed("Authorization header is missing.")

        # Remove the 'Bearer ' part if present
        if token.startswith("Bearer "):
            token = token[7:]

        # Decode the JWT token
        try:
            payload = jwt.decode(
                token,
                os.environ.get("JWT_SECRET_KEY"),
                algorithms=[os.environ.get("JWT_ALGORITHM")],
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        # Extract user_id from the token payload
        token_user_id = payload.get("user_id")

        # Ensure the user_id from query params matches
        # the user_id from the token
        # Filter the queryset by creator's user ID if user_id is present
        if user_id is not None and int(user_id) == token_user_id:
            queryset = queryset.filter(creator__id=user_id)
        else:
            raise AuthenticationFailed("User ID mismatch or missing.")

        return queryset

    # Override the list method to return the filtered queryset
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            content_type="application/json",
        )


class PlaylistDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, JSONParser]
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer