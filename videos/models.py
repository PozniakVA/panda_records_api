import pathlib
import uuid

from cloudinary_storage.storage import (
    VideoMediaCloudinaryStorage,
    MediaCloudinaryStorage
)
from django.db import models
from django.utils.text import slugify


def video_path(instance, filename):
    filename = (
        f"{slugify(instance.title)}-{uuid.uuid4()}"
        + pathlib.Path(filename).suffix
    )

    return f"endpoint_video/videos/{filename}"


def photo_path(instance, filename):
    filename = (
        f"{slugify(instance.title)}-{uuid.uuid4()}"
        + pathlib.Path(filename).suffix
    )
    return f"endpoint_video/photos/{filename}"


class Video(models.Model):
    title = models.CharField(max_length=100)
    description_block1 = models.TextField(blank=True, null=True)
    description_block2 = models.TextField(blank=True, null=True)
    poster = models.ImageField(
        upload_to=photo_path,
        storage=MediaCloudinaryStorage(),
        max_length=1000,
        null=True,
        blank=True,
    )
    video_file = models.FileField(
        upload_to=video_path,
        storage=VideoMediaCloudinaryStorage(),
        max_length=1000,
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return self.title
