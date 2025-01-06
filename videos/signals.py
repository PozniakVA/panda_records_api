from cloudinary.uploader import destroy
from django.db.models.signals import post_delete
from django.dispatch import receiver

from videos.models import Video


@receiver(post_delete, sender=Video)
def delete_associated_file(sender, instance, **kwargs):
    if instance.poster:
        file_url = instance.poster.url
        public_id = file_url.split("/v1/")[1]

        destroy(public_id)

    if instance.video_file:
        file_url = instance.video_file.url
        public_id = file_url.split("/v1/")[1]

        destroy(public_id, resource_type="video")
