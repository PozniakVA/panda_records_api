from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from songs.models import Song
from songs.serializer import SongSerializer


class SongsUnauthenticatedUserTestCase(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        self.url_list = reverse("songs:song-list")
        self.song = Song.objects.create(title="Test Song")

    def test_unauthenticated_user_can_get_data(self) -> None:

        """Test method GET"""

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = SongSerializer(self.song)
        self.assertEqual(response.data, [serializer.data])

    def test_unauthenticated_user_cannot_create_data(self) -> None:

        """Test method POST"""

        data = {"title": "Be Free", "artist": "Papa Roach"}

        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Song.objects.filter(title=data["title"]).exists())

    def test_unauthenticated_user_cannot_update_data(self) -> None:

        """Test method PATCH"""

        response = self.client.patch(
            reverse("songs:song-detail", kwargs={"pk": self.song.id}),
            data={"title": "Updated Song"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Song.objects.get(id=self.song.id).title, "Test Song")

    def test_unauthenticated_user_cannot_delete_data(self) -> None:

        """Test method DELETE"""

        response = self.client.delete(
            reverse("songs:song-detail", kwargs={"pk": self.song.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Song.objects.filter(id=self.song.id).exists())


class SongsAdminTestCase(TestCase):

    def setUp(self) -> None:

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="<PASSWORD>",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

        self.song = Song.objects.create(title="Test Song")

    def test_admin_can_create_data(self) -> None:

        """Test method POST"""

        response = self.client.post(
            reverse("songs:song-list"),
            {"title": "Be Free", "artist": "Papa Roach"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        song = Song.objects.get(id=response.data["id"])
        serializer = SongSerializer(song)
        self.assertEqual(serializer.data, response.data)

    def test_admin_can_update_data(self) -> None:

        """Test method PATCH"""

        response = self.client.patch(
            reverse("songs:song-detail", kwargs={"pk": self.song.id}),
            data={"title": "Updated Song"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Song.objects.filter(title="Updated Song").exists())

    def test_admin_can_delete_data(self) -> None:

        """Test method DELETE"""

        response_delete = self.client.delete(
            reverse("songs:song-detail", kwargs={"pk": self.song.id})
        )
        self.assertEqual(
            response_delete.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(Song.objects.filter(id=self.song.id).exists())


class SongFilterTestCase(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_filter_data(self) -> None:
        song_1 = Song.objects.create(
            title="Song_1",
            artist="Artist_1",
            top=True
        )
        serializer_1 = SongSerializer(song_1)

        song_2 = Song.objects.create(
            title="Song_2",
            artist="Artist_2",
        )
        serializer_2 = SongSerializer(song_2)

        response = self.client.get(
            reverse("songs:song-list"),
            {"top": True}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_1.data, response.data)
        self.assertNotIn(serializer_2.data, response.data)
