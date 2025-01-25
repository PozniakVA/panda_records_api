from cloudinary.uploader import destroy
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from services.models import Service


@receiver(post_delete, sender=Service)
def delete_associated_file(sender, instance, **kwargs):
    if instance.photo:
        file_url = instance.photo.url
        public_id = file_url.split("/v1/")[1]

        destroy(public_id)


@receiver(pre_save, sender=Service)
def delete_old_file_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_photo = Service.objects.get(pk=instance.pk).photo
    except Service.DoesNotExist:
        return

    new_file = instance.photo
    if old_photo and not old_photo == new_file:

        old_photo_url = old_photo.url
        public_id = old_photo_url.split("/v1/")[1]

        destroy(public_id)
