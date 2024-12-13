import re

from django.core.management.base import BaseCommand
from django_q.tasks import async_task

from notifications.bot import bot
from notifications.models import Notification


class Command(BaseCommand):
    """Launching a telegram bot."""

    def handle(self, *args, **options):
        self.stdout.write("Bot is running! Press Ctrl + C to stop the bot.")

        @bot.message_handler(commands=["start"])
        def bot_launch(message):
            async_task("notifications.tasks.connect_telegram_user_with_user_from_db", message)
            async_task("notifications.tasks.send_welcome_message", message)

        @bot.message_handler(commands=["stop_notifications", "start_notifications"])
        def toggle_notifications(message):
            if message.text == "/stop_notifications":
                async_task("notifications.tasks.stop_notifications", message)
            elif message.text == "/start_notifications":
                async_task("notifications.tasks.start_notifications", message)

        @bot.message_handler(commands=["all_commands", "help"])
        def call_show_all_commands(message):
            async_task("notifications.tasks.show_all_commands", message)

        @bot.callback_query_handler(func=lambda callback: True)
        def callback_handler(call):
            text = call.message.text
            match_status = re.search(r"Статус: (\w+)", text)
            match_id = re.search(r"ID: (\d+)", text)

            if not match_status or not match_id:
                bot.reply_to(call.message, "Схоже, щось пішло не так. Вказано неправильний формат повідомлення 😅")
                return

            notification_status = match_status.group(1)
            notification_id = match_id.group(1)

            try:
                notification = Notification.objects.get(id=notification_id)
            except Notification.DoesNotExist:
                bot.reply_to(call.message, "Повідомлення не знайдено в базі даних 😅")
                return
            if notification_status != Notification.NotificationStatus.COMPLETED.label:

                if call.data == "done":
                    notification.status = Notification.NotificationStatus.COMPLETED
                    send_notification(notification, Notification.NotificationStatus.COMPLETED.label)
                    bot.delete_message(call.message.chat.id, call.message.id)

                elif call.data == "in_process":
                    if notification_status != Notification.NotificationStatus.PROCESSING.label:
                        notification.status = Notification.NotificationStatus.PROCESSING
                        send_notification(notification, Notification.NotificationStatus.PROCESSING.label)
                        bot.delete_message(call.message.chat.id, call.message.id)
                    else:
                        bot.reply_to(call.message, "Замовлення вже в обробці 🔄")

            else:
                bot.reply_to(call.message, "Завдання вже виконано ✅")

        def send_notification(notification, status_label):
            async_task(
                "notifications.tasks.send_notification_to_admin_about_client",
                {
                    "id": notification.id,
                    "status": status_label,
                    "name": notification.name,
                    "email": notification.email,
                    "phone_number": notification.phone_number,
                    "created_at": str(notification.created_at),
                    "message": notification.message,
                },
            )


        bot.infinity_polling()

        self.stdout.write(self.style.SUCCESS("Telegram bot is stopped"))
