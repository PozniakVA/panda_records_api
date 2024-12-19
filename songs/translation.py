from modeltranslation.translator import register, TranslationOptions

from songs.models import Song


@register(Song)
class SongTranslationOptions(TranslationOptions):
    fields = ("title", "artist")
