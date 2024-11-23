import pathlib
import uuid
from django.db import models
from django.utils.text import slugify


def audio_path(instance, filename):
    filename = (
        f"{slugify(instance.title)}-{uuid.uuid4()}"
        + pathlib.Path(filename).suffix
    )

    return pathlib.Path("songs/images/") / filename

def image_path(instance, filename):
    filename = (
        f"{slugify(instance.title)}-{uuid.uuid4()}"
        + pathlib.Path(filename).suffix
    )

    return pathlib.Path("songs/audio/") / filename


class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to=audio_path)
    image = models.ImageField(upload_to=image_path, null=True, blank=True)

    def __str__(self) -> str:
        return self.title
