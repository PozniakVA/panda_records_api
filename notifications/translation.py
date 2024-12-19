from modeltranslation.translator import register, TranslationOptions

from notifications.models import Notification


@register(Notification)
class NotificationsTranslationOptions(TranslationOptions):
    fields = ("status", "name", "message")
