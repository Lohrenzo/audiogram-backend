from django.urls import path
from .views import (
    StreamRecordListCreateView,
    CalculateARSView,
    AudioTrackStreamCountView,
)

urlpatterns = [
    path(
        "stream",
        StreamRecordListCreateView.as_view(),
        name="create-stream",
    ),
    # path(
    #     "stream/artist/<int:artist_id>/count",
    #     ArtistStreamCountView.as_view(),
    #     name="artist-streams",
    # ),
    path(
        "stream/artist/<int:artist_id>/calculate-ars",
        CalculateARSView.as_view(),
        name="calculate-ars",
    ),
    path(
        "stream/audio/<int:audio_id>/count",
        AudioTrackStreamCountView.as_view(),
        name="audio-stream-count",
    ),
]
