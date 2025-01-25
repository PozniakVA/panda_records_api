from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from equipment.models import Equipment
from equipment.serializer import EquipmentSerializer


class EquipmentUnauthenticatedUserTestCase(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        self.url_list = reverse("equipment:equipment-list")
        self.equipment = Equipment.objects.create(name="Test Equipment")

    def test_unauthenticated_user_can_get_data(self) -> None:

        """Test method GET"""

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = EquipmentSerializer(self.equipment)
        self.assertEqual(response.data, [serializer.data])

    def test_unauthenticated_user_cannot_create_data(self) -> None:

        """Test method POST"""

        data = {"name": "Guitar", "model": "w3000"}

        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Equipment.objects.filter(name=data["name"], model=data["model"]).exists())

    def test_unauthenticated_user_cannot_update_data(self) -> None:

        """Test method PUT"""

        response = self.client.put(
            reverse("equipment:equipment-detail", kwargs={"pk": self.equipment.id}),
            data={"name": "Updated Equipment"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Equipment.objects.get(id=self.equipment.id).name, "Test Equipment")

    def test_unauthenticated_user_cannot_delete_data(self) -> None:

        """Test method DELETE"""

        response = self.client.delete(
            reverse("equipment:equipment-detail", kwargs={"pk": self.equipment.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Equipment.objects.filter(id=self.equipment.id).exists())


class EquipmentAdminTestCase(TestCase):

    def setUp(self) -> None:

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="<PASSWORD>",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

        self.equipment = Equipment.objects.create(name="Test Equipment")

    def test_admin_can_create_data(self) -> None:

        """Test method POST"""

        response = self.client.post(
            reverse("equipment:equipment-list"),
            {"name": "Guitar", "model": "w3000"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        equipment = Equipment.objects.get(id=response.data["id"])
        serializer = EquipmentSerializer(equipment)
        self.assertEqual(serializer.data, response.data)

    def test_admin_can_update_data(self) -> None:

        """Test method PUT"""

        response = self.client.put(
            reverse("equipment:equipment-detail", kwargs={"pk": self.equipment.id}),
            data={"name": "Updated Equipment"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Equipment.objects.filter(name="Updated Equipment").exists())

    def test_admin_can_delete_data(self) -> None:

        """Test method DELETE"""

        response_delete = self.client.delete(
            reverse("equipment:equipment-detail", kwargs={"pk": self.equipment.id})
        )
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Equipment.objects.filter(id=self.equipment.id).exists())
