from django.test import SimpleTestCase
from django.urls import resolve, reverse
from api.views import (
    AudioView,
    AudioDetail,
    PlaylistView,
    AlbumView,
    GenreView,
    LikesView,
)


class TestUrls(SimpleTestCase):

    def test_audio_url_is_resolved(self):
        url = reverse("audio")
        resolved_func = resolve(url).func
        # print("Resolved Funcfion: ", resolved_func)
        # Check that the resolved function's view class is
        # the expected view class
        self.assertEquals(resolved_func.view_class, AudioView)

    def test_audio_detail_url_is_resolved(self):
        url = reverse("audio_detail", args=[3])
        resolved_func = resolve(url).func
        # print("Resolved Funcfion: ", resolved_func)
        # Check that the resolved function's view class is
        # the expected view class
        self.assertEquals(resolved_func.view_class, AudioDetail)

    def test_genre_url_is_resolved(self):
        url = reverse("genre")
        resolved_func = resolve(url).func
        # Check that the resolved function's view class is
        # the expected view class
        self.assertEquals(resolved_func.view_class, GenreView)

    def test_album_url_is_resolved(self):
        url = reverse("album")
        resolved_func = resolve(url).func
        # Check that the resolved function's view class is
        # the expected view class
        self.assertEquals(resolved_func.view_class, AlbumView)

    def test_playlist_url_is_resolved(self):
        url = reverse("playlist")
        resolved_func = resolve(url).func
        # Check that the resolved function's view class is
        # the expected view class
        self.assertEquals(resolved_func.view_class, PlaylistView)

    def test_likes_url_is_resolved(self):
        url = reverse("likes")
        resolved_func = resolve(url).func
        # Check that the resolved function's view class is
        # the expected view class
        self.assertEquals(resolved_func.view_class, LikesView)

    print("------------\nTest For URLs Done \n------------")
