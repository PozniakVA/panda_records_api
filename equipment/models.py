import pathlib
import uuid

from cloudinary_storage.storage import MediaCloudinaryStorage
from django.db import models
from django.utils.text import slugify


def photo_path(instance, filename):
    filename = (
        f"{slugify(instance.name)}-{uuid.uuid4()}"
        + pathlib.Path(filename).suffix
    )

    return pathlib.Path("equipment/photos/") / filename

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to=photo_path,
        null=True,
        blank=True,
        max_length=1000
    )

    def __str__(self) -> str:
        return self.model
