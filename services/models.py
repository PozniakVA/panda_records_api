import pathlib
import uuid

from cloudinary_storage.storage import MediaCloudinaryStorage
from django.db import models
from django.utils.text import slugify


def photo_path(instance, filename):
    filename = (
        f"{slugify(instance.title)}-{uuid.uuid4()}"
        + pathlib.Path(filename).suffix
    )
    return f"services/photos/{filename}"

class Service(models.Model):
    title = models.CharField(max_length=255)
    details_block1 = models.TextField(blank=True, null=True)
    details_block2 = models.TextField(blank=True, null=True)
    photo = models.ImageField(
        upload_to=photo_path,
        storage=MediaCloudinaryStorage(),
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return self.title