import os
from datetime import datetime

from django.contrib.auth import get_user_model
from telebot import types

from notifications.bot import bot
from notifications.models import Chat, Notification


def send_welcome_message(message):
    bot.send_message(
        message.chat.id,
        """
👋 Привіт! 👋
Я 𝗣𝗮𝗻𝗱𝗮𝗥𝗲𝗰𝗼𝗿𝗱𝘀𝗕𝗼𝘁, ваш помічник.
Я повідомлятиму вас щоразу, коли користувачі захочуть зв’язатися з вами щодо послуг PandaRecords.

Якщо хочете переглянути та зрозуміти всі команди, використайте:
➪ /all_commands
        """
    )


def connect_telegram_user_with_user_from_db(message):

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "Сторінка адміністратора",
            url=f"https://{os.getenv("DOMAIN")}/api/admin/"
        )
    )

    text = message.text.split()
    if len(text) > 1:
        token = message.text.split()[1]
        user = get_user_model().objects.get(token=token)
        Chat.objects.create(user=user, chat_id=message.chat.id)
    else:
        bot.send_message(
            message.chat.id,
            """
⚠️ Якщо у вас виникли проблеми з отриманням повідомлень, будь ласка, повторно
 увійдіть до бота, скориставшись посиланням, доступним на сторінці адміністратора
""", reply_markup=markup
        )


def send_notification_to_admin_about_client(notification):

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "Позначити як виконане",
            callback_data="done"
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            "Позначити як в процесі",
            callback_data="in_process"
        )
    )

    chats = Chat.objects.filter(
        user__is_staff=True,
        chat_id__isnull=False,
        notify_allowed=True,
    )

    created_at = datetime.fromisoformat(notification["created_at"])
    formatted_date = created_at.strftime("%d %B %Y, %H:%M")

    if notification["status"] == Notification.NotificationStatus.PENDING.label:
        title = "🔔 Нове сповіщення! 🔔"
    elif notification["status"] == Notification.NotificationStatus.PROCESSING.label:
        title = "🔄 В процесі обробки 🔄"
    else:
        title = "✅ Виконано ✅"

    for chat in chats:
        try:
            bot.send_message(
                chat.chat_id,
                f"""
{title}

ID: {notification["id"]}
Статус: {notification["status"]}

Ім'я клієнта ➪ {notification["name"]}
Email ➪ {notification["email"]}
Номер телефону ➪ {notification["phone_number"]}

Час запиту ➪ {formatted_date}

⬇️ Повідомлення ⬇️
{notification["message"]}
""", reply_markup=markup
            )
        except Exception as e:
            print(f"Failed to send the message to the chat {chat.chat_id}: {e}")

def stop_notifications(message):
    chat = Chat.objects.get(chat_id=message.chat.id)
    chat.notify_allowed = True

    bot.send_message(
        message.chat.id,
        """
🔕 Повідомлення вимкнено 🔕
Тепер ви не отримуватимете сповіщення про клієнтів, які хочуть зв’язатися з PandaRecords.

🔔 Увімкнути повідомлення 🔔
Якщо ви хочете знову отримувати сповіщення, скористайтеся командою:
➪ /start_notifications
        """
    )


def start_notifications(message):
    chat = Chat.objects.get(chat_id=message.chat.id)
    chat.notify_allowed = False

    bot.send_message(
        message.chat.id,
        """
🔔 Повідомлення увімкнено 🔔
Тепер ви почнете отримувати сповіщення від клієнтів, які бажають зв’язатися з PandaRecords.

🔕 Зупинити повідомлення 🔕
Якщо ви більше не хочете отримувати сповіщення, просто використайте команду:
➪ /stop_notifications
        """
    )


def show_all_commands(message):
    bot.send_message(
        message.chat.id,
        """
➪ /all_commands, /help
📝 Перегляд усіх команд із поясненнями

➪ /total_new_notifications
📊 Показує кількість нових повідомлень та повідомлень, які обробляються

➪ /stop_notifications
⛔ Вимкнення сповіщень

➪ /start_notifications
🔔 Увімкнення сповіщень

➪ /start
🚀 Початок роботи з ботом
"""
    )


def total_new_notifications(message):
    new_notifications = len(
        Notification.objects.filter(
            status=Notification.NotificationStatus.PENDING
        )
    )
    processing_notifications = len(
        Notification.objects.filter(
            status=Notification.NotificationStatus.PROCESSING
        )
    )

    bot.send_message(
        message.chat.id,
        f"""
Кількість нових повідомлень ➪ 🆕  {new_notifications}  🆕

Кількість повідомлень, які розглядаються ➪ 🔄  {processing_notifications}  🔄
"""
    )
