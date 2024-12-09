from datetime import datetime

from django.contrib.auth import get_user_model

from notifications.bot import bot
from notifications.models import Chat


def send_welcome_message(message):
    bot.send_message(
        message.chat.id,
        """
👋 Hello! I’m PandaRecordsBot, your assistant.
I’ll notify you every time users want to get in touch with you about PandaRecords services

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
⚠️ If you have issues receiving messages, please re-enter the bot using the link on the admin page
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
🔔 New Notification!
ID: {notification["id"]}
Status: {notification["status"]}

📢 A client wants to contact the administration!

👤 Client's Name: {notification["name"]}
📧 Email: {notification["email"]}
📞 Phone Number: {notification["phone_number"]}
🕒 Time of Request: {formatted_date}

💬 Message:
{notification["message"]}
"""
        )

def stop_notifications(message):
    chat = Chat.objects.get(chat_id=message.chat.id)
    chat.notify_allowed = True

    bot.send_message(
        message.chat.id,
        """
🔕 Notifications Disabled
Now you will not receive notifications about customers who want to contact PandaRecords.

🔔 Enable Notifications
If you want to start receiving notifications again, use the command:
/start_notifications
        """
    )

def start_notifications(message):
    chat = Chat.objects.get(chat_id=message.chat.id)
    chat.notify_allowed = False

    bot.send_message(
        message.chat.id,
        """
🔔 Notifications Activated!
Now you will start receiving notifications about customers who want to contact PandaRecords.

🚫 Stop Notifications
If you no longer wish to receive notifications, simply use the command:
/stop_notifications
        """
    )

def show_all_commands(message):
    bot.send_message(
        message.chat.id,
        """
🎨 /all_commands, /help
📝 View all commands and their explanations

🔕 /stop_notifications
⛔ Disable notifications

🔔 /start_notifications
🔄 Enable notifications

🚀 /start
🎉 Start interacting with the bot
        """
    )

