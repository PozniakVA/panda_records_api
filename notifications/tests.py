from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from notifications.models import Notification
from notifications.serializer import NotificationSerializer


class NotificationsUnauthenticatedUserTestCase(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        self.url_list = reverse("notifications:notification-list")
        self.data = {
            "name": "Levi",
            "email": "levi@gmail.com",
            "phone_number": "4657047032",
            "message": "Test Message",
        }
        self.notification = Notification.objects.create(**self.data)

    def test_unauthenticated_user_can_create_data(self) -> None:

        """Test method POST"""

        response = self.client.post(self.url_list, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Notification.objects.filter(name=self.data["name"]).exists())

    def test_unauthenticated_user_cannot_get_data(self) -> None:

        """Test method GET"""

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_update_data(self) -> None:

        """Test method PATCH"""

        response = self.client.patch(
            reverse("services:service-detail", kwargs={"pk": self.notification.id}),
            data={"name": "Updated"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Notification.objects.get(id=self.notification.id).name, "Levi")

    def test_unauthenticated_user_cannot_delete_data(self) -> None:

        """Test method DELETE"""

        response = self.client.delete(
            reverse("services:service-detail", kwargs={"pk": self.notification.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Notification.objects.filter(id=self.notification.id).exists())


class NotificationsAdminTestCase(TestCase):

    def setUp(self) -> None:

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="<PASSWORD>",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

        self.url_list = reverse("notifications:notification-list")
        self.data = {
            "name": "Levi",
            "email": "levi@gmail.com",
            "phone_number": "4657047032",
            "message": "Test Message",
        }
        self.notification = Notification.objects.create(**self.data)

    def test_admin_can_create_data(self) -> None:
        """Test method POST"""

        response = self.client.post(self.url_list, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Notification.objects.filter(name=self.data["name"]).exists())

    def test_admin_can_get_data(self) -> None:

        """Test method GET"""

        serializer = NotificationSerializer(self.notification)
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [serializer.data])
