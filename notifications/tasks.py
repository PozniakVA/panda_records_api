from datetime import datetime

from django.contrib.auth import get_user_model

from notifications.bot import bot
from notifications.models import Chat


def send_welcome_message(message):
    bot.send_message(
        message.chat.id,
        """
Hello! I’m PandaRecordsBot, your assistant. 
I’ll notify you every time users want to get in touch with you 
about PandaRecords services.

If you want to view and understand all the commands, use:
/all_commands
        """
    )

def connect_telegram_user_with_user_from_db(message):
    text = message.text.split()
    if len(text) > 1:
        token = message.text.split()[1]
        user = get_user_model().objects.get(token=token)
        Chat.objects.create(user=user, chat_id=message.chat.id)
    else:
        bot.send_message(
            message.chat.id,
            """
If you have issues receiving messages, please re-enter the bot
using the link
"""
        )

def send_notification_to_admin_about_client(notification):
    chats = Chat.objects.filter(
        user__is_staff=True,
        chat_id__isnull=False,
        notify_allowed=True,
    )

    created_at = datetime.fromisoformat(notification["created_at"])
    formatted_date = created_at.strftime("%d %B %Y, %H:%M")

    for chat in chats:
        bot.send_message(
            chat.chat_id,
            f"""
id: {notification["id"]}
status: {notification["status"]}
A client wants to contact the administration!
Client's name: {notification["name"]}
Email: {notification["email"]}
Phone number: {notification["phone_number"]}
Time of request: {formatted_date}
Message:
{notification["message"]}
"""
        )

def stop_notifications(message):
    chat = Chat.objects.get(chat_id=message.chat.id)
    chat.notify_allowed = True

    bot.send_message(
        message.chat.id,
        """
Now you will not receive notifications about customers who want to contact PandaRecords.
If you want to receive notifications, use the command /start_notifications
        """
    )

def start_notifications(message):
    chat = Chat.objects.get(chat_id=message.chat.id)
    chat.notify_allowed = False

    bot.send_message(
        message.chat.id,
        """
Now you will start receiving notifications about customers who want to contact PandaRecords.
If you want to stop receiving notifications, use the command /stop_notifications
        """
    )

def show_all_commands(message):
    bot.send_message(
        message.chat.id,
        """
/all_commands, /help — lists all commands with explanations.
/stop_notifications — stops notifications.
/start_notifications — resumes notifications.
/start — starts interaction with the bot.
        """
    )

