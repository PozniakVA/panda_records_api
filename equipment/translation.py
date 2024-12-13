from modeltranslation.translator import register, TranslationOptions

from equipment.models import Equipment


@register(Equipment)
class EquipmentTranslationOptions(TranslationOptions):
    fields = ("name",)
