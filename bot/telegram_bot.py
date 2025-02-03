import telebot
import requests

BOT_TOKEN = "7840749042:AAGA57FKu-6lqk81Zbzogwx0UL5kKdQ-sWA"
ADMIN_CHAT_ID = "7957686804"
bot = telebot.TeleBot(BOT_TOKEN)


# 📌 1. Пересылаем сообщения админу
@bot.message_handler(func=lambda msg: msg.chat.id != int(ADMIN_CHAT_ID))
def forward_to_admin(msg):
    bot.forward_message(ADMIN_CHAT_ID, msg.chat.id, msg.message_id)


# 📌 2. Админ может ответить
@bot.message_handler(commands=["reply"])
def reply_to_user(msg):
    parts = msg.text.split(" ", 2)
    if len(parts) < 3:
        bot.send_message(ADMIN_CHAT_ID, "❌ Используйте: /reply <user_id> <сообщение>")
        return

    user_id, text = parts[1], parts[2]
    bot.send_message(user_id, text)
    bot.send_message(ADMIN_CHAT_ID, "✅ Ответ отправлен.")


bot.polling()
