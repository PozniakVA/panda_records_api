import pathlib
import uuid

from django.db import models
from django.utils.text import slugify


def video_path(instance, filename):
    filename = (
        f"{slugify(instance.title)}-{uuid.uuid4()}"
        + pathlib.Path(filename).suffix
    )

    return pathlib.Path("lessons/videos/") / filename

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description_block1 = models.TextField(blank=True, null=True)
    description_block2 = models.TextField(blank=True, null=True)
    video_file = models.FileField(upload_to="video_path")

    def __str__(self) -> str:
        return self.title
