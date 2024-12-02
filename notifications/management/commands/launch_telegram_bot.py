from django.core.management.base import BaseCommand

from notifications.bot import bot
from notifications.tasks import (
    send_welcome_message,
    connect_telegram_user_with_user_from_db
)


class Command(BaseCommand):
    """Launching a telegram bot."""

    def handle(self, *args, **options):
        self.stdout.write("Bot is running! Press Ctrl + C to stop the bot.")

        @bot.message_handler(commands=["start"])
        def bot_launch(message):
            connect_telegram_user_with_user_from_db(message)
            send_welcome_message(message)

        bot.infinity_polling()

        self.stdout.write(self.style.SUCCESS("Telegram bot is stopped"))
