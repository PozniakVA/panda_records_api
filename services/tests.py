from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from services.models import Service
from services.serializer import ServiceSerializer


class ServicesUnauthenticatedUserTestCase(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        self.url_list = reverse("services:service-list")
        self.service = Service.objects.create(title="Test Service")

    def test_unauthenticated_user_can_get_data(self) -> None:

        """Test method GET"""

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = ServiceSerializer(self.service)
        self.assertEqual(response.data, [serializer.data])

    def test_unauthenticated_user_cannot_create_data(self) -> None:

        """Test method POST"""

        data = {"title": "Equipment rental",}

        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Service.objects.filter(title=data["title"]).exists())

    def test_unauthenticated_user_cannot_update_data(self) -> None:

        """Test method PUT"""

        response = self.client.put(
            reverse("services:service-detail", kwargs={"pk": self.service.id}),
            data={"title": "Updated Service"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Service.objects.get(id=self.service.id).title, "Test Service")

    def test_unauthenticated_user_cannot_delete_data(self) -> None:

        """Test method DELETE"""

        response = self.client.delete(
            reverse("services:service-detail", kwargs={"pk": self.service.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Service.objects.filter(id=self.service.id).exists())


class ServicesEquipmentAdminTestCase(TestCase):

    def setUp(self) -> None:

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="<PASSWORD>",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

        self.service = Service.objects.create(title="Test Service")

    def test_admin_can_create_data(self) -> None:

        """Test method POST"""

        response = self.client.post(
            reverse("services:service-list"),
            {"title": "Equipment rental",}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        service = Service.objects.get(id=response.data["id"])
        serializer = ServiceSerializer(service)
        self.assertEqual(serializer.data, response.data)

    def test_admin_can_update_data(self) -> None:

        """Test method PUT"""

        response = self.client.put(
            reverse("services:service-detail", kwargs={"pk": self.service.id}),
            data={"title": "Updated Service"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Service.objects.filter(title="Updated Service").exists())

    def test_admin_can_delete_data(self) -> None:

        """Test method DELETE"""

        response_delete = self.client.delete(
            reverse("services:service-detail", kwargs={"pk": self.service.id})
        )
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Service.objects.filter(id=self.service.id).exists())
