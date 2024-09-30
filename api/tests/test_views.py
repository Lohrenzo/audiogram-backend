from django.test import TestCase, Client
from django.urls import reverse
from api.models import (
    Audio,
    Album,
    Genre,
)
from authentication.models import User

# from django.contrib.auth.models import User


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(
            email="testuser@test.com",
            first_name="Test",
            username="testuser",
            password="12345",
            is_artist=False,
        )
        self.client.login(username="testuser", password="12345")

        # Create test genre, album, and audio
        self.genre = Genre.objects.create(title="Pop")
        self.album = Album.objects.create(title="Test Album", artist=self.user)
        self.audio = Audio.objects.create(
            title="Test Audio",
            artist=self.user,
            album=self.album,
            genre=self.genre,
        )

        # URLs
        self.audio_url = reverse("audio")
        self.audio_detail_url = reverse("audio_detail", args=[self.audio.pk])

    def test_audio_view_GET(self):
        """
        Purpose: Testing the GET method of the audio view
        It should return a list of audio objects.
        """
        response = self.client.get(self.audio_url)

        print("Response Content: ", response)

        self.assertEquals(response.status_code, 200)
        self.assertEqual(
            len(response.json()), 1
        )  # Expecting 1 audio object in response
        self.assertEqual(response.json()[0]["title"], self.audio.title)

    def test_audio_detail_view_GET(self):
        """
        Purpose: Testing the GET method of the audio detail view.
        It should return the details of a specific audio object.
        """
        response = self.client.get(self.audio_detail_url)

        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.json()["title"], self.audio.title)
        self.assertEqual(response.json()["artist"], self.user.username)

    def test_audio_view_no_auth(self):
        """
        Test to ensure that the audio view is
        protected and requires authentication.
        """
        self.client.logout()
        response = self.client.get(self.audio_url)
        self.assertEquals(
            response.status_code, 401
        )  # Should return unauthprized for unauthenticated users

    print("------------\nTest For Views Done \n------------")
