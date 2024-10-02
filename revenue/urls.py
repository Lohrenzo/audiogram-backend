from django.urls import path
from .views import (
    StreamRecordCreateView,
    AllStreamsView,
    ArtistStreamsView,
    CalculateARSView,
)

urlpatterns = [
    path("streams/", StreamRecordCreateView.as_view(), name="create-stream"),
    path("streams/all/", AllStreamsView.as_view(), name="all-streams"),
    path(
        "streams/artist/<int:artist_id>/",
        ArtistStreamsView.as_view(),
        name="artist-streams",
    ),
    path(
        "streams/artist/<int:artist_id>/calculate-ars/",
        CalculateARSView.as_view(),
        name="calculate-ars",
    ),
]
