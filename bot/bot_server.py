from flask import Flask, request, jsonify
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import time

app = Flask(__name__)

# Telegram API
BOT_TOKEN = "7840749042:AAGA57FKu-6lqk81Zbzogwx0UL5kKdQ-sWA"
ADMIN_CHAT_ID = "7957686804"

# Хранилище подписчиков на напоминания
subscribers = {}

# Функция отправки сообщений в Telegram
def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

# 📌 1. Обработчик формы с сайта
@app.route("/submit_form", methods=["POST"])
def submit_form():
    data = request.json
    message = (f"🚗 Новая запись на СТО!\n\n"
               f"👤 ФИО: {data['name']}\n"
               f"📞 Телефон: {data['phone']}\n"
               f"✉️ Почта: {data['email']}\n"
               f"📟 Telegram: @{data['telegram'] if data['telegram'] else 'Не указан'}")

    send_telegram_message(ADMIN_CHAT_ID, message)
    return jsonify({"status": "ok", "message": "Заявка отправлена!"})

# 📌 2. Подписка на напоминания
@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.json
    chat_id = data["chat_id"]
    subscribers[chat_id] = time.time()
    send_telegram_message(chat_id, "✅ Вы подписаны на ежемесячные напоминания!")
    return jsonify({"status": "subscribed"})

# 📌 3. Отписка от напоминаний
@app.route("/unsubscribe", methods=["POST"])
def unsubscribe():
    data = request.json
    chat_id = data["chat_id"]
    if chat_id in subscribers:
        del subscribers[chat_id]
        send_telegram_message(chat_id, "❌ Вы отписались от напоминаний.")
    return jsonify({"status": "unsubscribed"})

# 📌 4. Функция отправки напоминаний (раз в месяц)
def send_monthly_reminders():
    for chat_id in subscribers:
        send_telegram_message(chat_id, "🚗 Напоминание! Пора пройти техобслуживание.")

# Запускаем планировщик
scheduler = BackgroundScheduler()
scheduler.add_job(send_monthly_reminders, "interval", weeks=4)
scheduler.start()

if __name__ == "__main__":
    app.run(port=5000)
