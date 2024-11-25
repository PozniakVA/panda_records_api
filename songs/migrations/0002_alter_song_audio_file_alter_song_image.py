# Generated by Django 5.1.3 on 2024-11-25 13:00

import songs.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("songs", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="song",
            name="audio_file",
            field=models.FileField(upload_to=songs.models.audio_path),
        ),
        migrations.AlterField(
            model_name="song",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to=songs.models.image_path
            ),
        ),
    ]