from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from lessons.models import Lesson
from lessons.serializer import LessonSerializer


class LessonUnauthenticatedUserTestCase(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

        self.url_list = reverse("lessons:lesson-list")
        self.lesson = Lesson.objects.create(title="Test Lesson")

    def test_unauthenticated_user_can_get_data(self) -> None:

        """Test method GET"""

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = LessonSerializer(self.lesson)
        self.assertEqual(response.data, [serializer.data])

    def test_unauthenticated_user_cannot_create_data(self) -> None:

        """Test method POST"""

        data = {"title": "Playing the guitar",}

        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Lesson.objects.filter(title=data["title"]).exists())

    def test_unauthenticated_user_cannot_update_data(self) -> None:

        """Test method PUT"""

        response = self.client.put(
            reverse("lessons:lesson-detail", kwargs={"pk": self.lesson.id}),
            data={"title": "Updated Lesson"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Lesson.objects.get(id=self.lesson.id).title, "Test Lesson")

    def test_unauthenticated_user_cannot_delete_data(self) -> None:

        """Test method DELETE"""

        response = self.client.delete(
            reverse("lessons:lesson-detail", kwargs={"pk": self.lesson.id})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Lesson.objects.filter(id=self.lesson.id).exists())


class LessonEquipmentAdminTestCase(TestCase):

    def setUp(self) -> None:

        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="<PASSWORD>",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

        self.lesson = Lesson.objects.create(title="Test Lesson")

    def test_admin_can_create_data(self) -> None:

        """Test method POST"""

        response = self.client.post(
            reverse("lessons:lesson-list"),
            {"title": "Playing the guitar",}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        lesson = Lesson.objects.get(id=response.data["id"])
        serializer = LessonSerializer(lesson)
        self.assertEqual(serializer.data, response.data)

    def test_admin_can_update_data(self) -> None:

        """Test method PUT"""

        response = self.client.put(
            reverse("lessons:lesson-detail", kwargs={"pk": self.lesson.id}),
            data={"title": "Updated Lesson"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Lesson.objects.filter(title="Updated Lesson").exists())

    def test_admin_can_delete_data(self) -> None:

        """Test method DELETE"""

        response_delete = self.client.delete(
            reverse("lessons:lesson-detail", kwargs={"pk": self.lesson.id})
        )
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())
