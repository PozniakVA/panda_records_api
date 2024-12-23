from modeltranslation.translator import register, TranslationOptions

from services.models import Service


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ("title", "details_block1", "details_block2", "details_block3")
