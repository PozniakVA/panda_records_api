from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from videos.models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "description_block1",
            "description_block2",
            "poster",
            "video_file"
        ]

    def validate_poster(self, value):
        if value and value.size > 10 * 1024 * 1024:  # 10 MB
            raise ValidationError("File size must not be greater than 10 MB.")
        return value

    def validate_video_file(self, value):
        if value and value.size > 100 * 1024 * 1024:  # 100 MB
            raise ValidationError("File size must not be greater than 100 MB.")
        return value
