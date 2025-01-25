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
    title = models.CharField(max_length=250)
    details_block1 = models.TextField(blank=True, null=True)
    details_block2 = models.TextField(blank=True, null=True)
    details_block3 = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    hourly = models.BooleanField(blank=True, null=True)
    photo = models.ImageField(
        upload_to=photo_path,
        storage=MediaCloudinaryStorage(),
        blank=True,
        null=True,
        max_length=1000,
    )

    def __str__(self) -> str:
        return self.title
