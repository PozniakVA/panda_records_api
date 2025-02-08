import pathlib
import uuid

import cloudinary.uploader
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.db import models, transaction
from django.utils.text import slugify


def photo_path(instance, filename):
    filename = (
        f"{slugify(instance.title)}-{uuid.uuid4()}"
        + pathlib.Path(filename).suffix
    )
    return f"songs/photos/{filename}"


def audio_path(instance, filename):
    filename = (
        f"{slugify(instance.title)}-{uuid.uuid4()}"
        + pathlib.Path(filename).suffix
    )
    return f"songs/audio/{filename}"


class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    audio_file = models.FileField(
        upload_to=audio_path,
        max_length=1000,
        null=True,
        blank=True,
    )
    photo = models.ImageField(
        upload_to=photo_path,
        storage=MediaCloudinaryStorage(),
        max_length=1000,
        null=True,
        blank=True,
    )
    duration = models.PositiveIntegerField(null=True, blank=True)
    top = models.BooleanField(default=False)

    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.audio_file and not self.duration:

            response = cloudinary.uploader.upload(
                self.audio_file,
                resource_type="video"
            )

            duration = response.get("duration")
            self.duration = duration

            super().save(update_fields=["duration"])

    def __str__(self) -> str:
        return self.title
