from cloudinary.uploader import destroy
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from songs.models import Song


@receiver(post_delete, sender=Song)
def delete_associated_file(sender, instance, **kwargs):
    if instance.photo:
        file_url = instance.photo.url
        public_id = file_url.split("/v1/")[1]

        destroy(public_id)

    if instance.audio_file:
        file_url = instance.audio_file.url
        public_id = file_url.split("/v1/")[1]

        destroy(public_id, resource_type="raw")


@receiver(pre_save, sender=Song)
def delete_old_file_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        song = Song.objects.get(pk=instance.pk)
        old_photo = song.photo
        old_audio_file = song.audio_file

    except Song.DoesNotExist:
        return

    new_photo = instance.photo
    if not old_photo == new_photo:

        old_photo_url = old_photo.url
        public_id = old_photo_url.split("/v1/")[1]

        destroy(public_id)

    new_audio_file = instance.audio_file
    if not old_audio_file == new_audio_file:
        old_audio_file_url = old_audio_file.url
        public_id = old_audio_file_url.split("/v1/")[1]
        destroy(public_id, resource_type="raw")
