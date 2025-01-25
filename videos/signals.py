from cloudinary.uploader import destroy
from django.db.models.signals import post_delete, pre_save
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


@receiver(pre_save, sender=Video)
def delete_old_file_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        video = Video.objects.get(pk=instance.pk)
        old_poster = video.poster
        old_video_file = video.video_file

    except Video.DoesNotExist:
        return

    new_poster = instance.poster
    if old_poster and not old_poster == new_poster:

        old_poster_url = old_poster.url
        public_id = old_poster_url.split("/v1/")[1]

        destroy(public_id)

    new_video_file = instance.video_file
    if old_video_file and not old_video_file == new_video_file:
        old_video_file_url = old_video_file.url
        public_id = old_video_file_url.split("/v1/")[1]
        destroy(public_id, resource_type="video")
