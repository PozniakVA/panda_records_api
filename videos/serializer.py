from rest_framework import serializers

from videos.models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "description_block1",
            "description_block2",
            "video_file"
        ]
