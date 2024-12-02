from django.core.management.base import BaseCommand

from notifications.bot import bot
from notifications.tasks import (
    send_welcome_message,
    connect_telegram_user_with_user_from_db, stop_notifications, start_notifications, show_all_commands
)


class Command(BaseCommand):
    """Launching a telegram bot."""

    def handle(self, *args, **options):
        self.stdout.write("Bot is running! Press Ctrl + C to stop the bot.")

        @bot.message_handler(commands=["start"])
        def bot_launch(message):
            connect_telegram_user_with_user_from_db(message)
            send_welcome_message(message)

        @bot.message_handler(commands=["stop_notifications", "start_notifications"])
        def toggle_notifications(message):
            if message.text == "/stop_notifications":
                stop_notifications(message)
            elif message.text == "/start_notifications":
                start_notifications(message)

        @bot.message_handler(commands=["all_commands", "help"])
        def call_show_all_commands(message):
            show_all_commands(message)

        bot.infinity_polling()

        self.stdout.write(self.style.SUCCESS("Telegram bot is stopped"))
