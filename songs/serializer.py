from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from songs.models import Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = [
            "id",
            "title",
            "artist",
            "audio_file",
            "photo",
            "duration",
            "top"
        ]

    def validate_audio_file(self, value):
        if value and value.size > 10 * 1024 * 1024:  # 10 MB
            raise ValidationError("File size must not be greater than 10 MB.")
        return value

    def validate_photo(self, value):
        if value and value.size > 10 * 1024 * 1024:  # 10 MB
            raise ValidationError("File size must not be greater than 10 MB.")
        return value
