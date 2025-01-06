from cloudinary.uploader import destroy
from django.db.models.signals import post_delete
from django.dispatch import receiver

from services.models import Service


@receiver(post_delete, sender=Service)
def delete_associated_file(sender, instance, **kwargs):
    if instance.photo:
        file_url = instance.photo.url
        public_id = file_url.split("/v1/")[1]

        destroy(public_id)
