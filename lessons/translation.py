from modeltranslation.translator import register, TranslationOptions

from lessons.models import Lesson


@register(Lesson)
class LessonTranslationOptions(TranslationOptions):
    fields = ("title", "description_block1", "description_block2")
