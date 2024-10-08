# import django_eventstream
from django.urls import path
from .views import (
    AlbumView,
    AlbumDetail,
    UserAlbumsView,
    UserAudiosView,
    AudioDetail,
    AudioView,
    GenreView,
    LikesView,
    PlaylistDetail,
    PlaylistView,
    UserPlaylistsView,
    increment_play_count,
)

urlpatterns = [
    path("audio", AudioView.as_view(), name="audio"),
    path(
        "audio/<int:pk>",
        AudioDetail.as_view(),
        name="audio_detail",
    ),
    path(
        "audio/<int:audio_id>/play/",
        increment_play_count,
        name="increment_play_count",
    ),
    path("user/audios", UserAudiosView.as_view(), name="user-audios"),
    path("genre", GenreView.as_view(), name="genre"),
    path("album", AlbumView.as_view(), name="album"),
    path(
        "album/<int:pk>",
        AlbumDetail.as_view(),
        name="album_detail",
    ),
    path("user/albums", UserAlbumsView.as_view(), name="user-albums"),
    path("likes", LikesView.as_view(), name="likes"),
    path("playlist", PlaylistView.as_view(), name="playlist"),
    path(
        "playlist/<int:pk>",
        PlaylistDetail.as_view(),
        name="playlist_detail",
    ),
    path("user/playlists", UserPlaylistsView.as_view(), name="user-playlists"),
    # path("events", include(django_eventstream.urls), {"channels": ["test"]}),
]
