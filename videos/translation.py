from modeltranslation.translator import register, TranslationOptions

from videos.models import Video


@register(Video)
class VideoTranslationOptions(TranslationOptions):
    fields = ("title", "description_block1", "description_block2")
