# Generated by Django 5.1.3 on 2024-12-19 12:57

import cloudinary_storage.storage
import videos.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Lesson",
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
                ("title", models.CharField(max_length=100)),
                ("title_en", models.CharField(max_length=100, null=True)),
                ("title_uk", models.CharField(max_length=100, null=True)),
                ("description_block1", models.TextField(blank=True, null=True)),
                ("description_block1_en", models.TextField(blank=True, null=True)),
                ("description_block1_uk", models.TextField(blank=True, null=True)),
                ("description_block2", models.TextField(blank=True, null=True)),
                ("description_block2_en", models.TextField(blank=True, null=True)),
                ("description_block2_uk", models.TextField(blank=True, null=True)),
                (
                    "video_file",
                    models.FileField(
                        blank=True,
                        max_length=1000,
                        null=True,
                        storage=cloudinary_storage.storage.VideoMediaCloudinaryStorage(),
                        upload_to=videos.models.video_path,
                    ),
                ),
            ],
        ),
    ]