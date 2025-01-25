# Generated by Django 5.1.3 on 2024-12-14 18:17

import cloudinary_storage.storage
import equipment.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Equipment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("name_en", models.CharField(max_length=100, null=True)),
                ("name_uk", models.CharField(max_length=100, null=True)),
                ("model", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        max_length=1000,
                        null=True,
                        storage=cloudinary_storage.storage.MediaCloudinaryStorage(),
                        upload_to=equipment.models.photo_path,
                    ),
                ),
            ],
        ),
    ]
