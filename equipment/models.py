import pathlib
import uuid

from django.db import models
from django.utils.text import slugify


def image_path(instance, filename):
    filename = (
        f"{slugify(instance.name)}-{uuid.uuid4()}"
        + pathlib.Path(filename).suffix
    )

    return pathlib.Path("equipment/images/") / filename

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to=image_path, null=True, blank=True)

    def __str__(self) -> str:
        return self.model
