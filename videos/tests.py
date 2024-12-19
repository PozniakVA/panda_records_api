from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from videos.models import Video
from videos.serializer import VideoSerializer


class VideoUnauthenticatedUserTestCase(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        self.url_list = reverse("videos:video-list")
        self.video = Video.objects.create(title="Test Video")

    def test_unauthenticated_user_can_get_data(self) -> None:

        """Test method GET"""

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = VideoSerializer(self.video)
        self.assertEqual(response.data, [serializer.data])

    def test_unauthenticated_user_cannot_create_data(self) -> None:

        """Test method POST"""

        data = {"title": "Playing the guitar",}

        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Video.objects.filter(title=data["title"]).exists())

    def test_unauthenticated_user_cannot_update_data(self) -> None:

        """Test method PUT"""

        response = self.client.put(
            reverse("videos:video-detail", kwargs={"pk": self.video.id}),
            data={"title": "Updated Video"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Video.objects.get(id=self.video.id).title, "Test Video")

    def test_unauthenticated_user_cannot_delete_data(self) -> None:

        """Test method DELETE"""

        response = self.client.delete(
            reverse("videos:video-detail", kwargs={"pk": self.video.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Video.objects.filter(id=self.video.id).exists())


class VideoEquipmentAdminTestCase(TestCase):

    def setUp(self) -> None:

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="<PASSWORD>",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

        self.video = Video.objects.create(title="Test Video")

    def test_admin_can_create_data(self) -> None:

        """Test method POST"""

        response = self.client.post(
            reverse("videos:video-list"),
            {"title": "Playing the guitar",}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        video = Video.objects.get(id=response.data["id"])
        serializer = VideoSerializer(video)
        self.assertEqual(serializer.data, response.data)

    def test_admin_can_update_data(self) -> None:

        """Test method PUT"""

        response = self.client.put(
            reverse("videos:video-detail", kwargs={"pk": self.video.id}),
            data={"title": "Updated Video"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Video.objects.filter(title="Updated Video").exists())

    def test_admin_can_delete_data(self) -> None:

        """Test method DELETE"""

        response_delete = self.client.delete(
            reverse("videos:video-detail", kwargs={"pk": self.video.id})
        )
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Video.objects.filter(id=self.video.id).exists())
