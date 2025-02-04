from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

ADMIN_CHAT_ID = "7957686804"
TELEGRAM_TOKEN = "7840749042:AAGA57FKu-6lqk81Zbzogwx0UL5kKdQ-sWA"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

app = Flask(__name__)

# Дозволяємо доступ лише з певного джерела (локальний клієнт)
CORS(app, resources={r"/*": {"origins": "http://localhost:63342"}})

@app.route("/submit_form", methods=["POST", "OPTIONS"])
def submit_form():
    # Відповідь на preflight (OPTIONS) запит
    if request.method == "OPTIONS":
        response = jsonify()
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:63342"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    # Основний обробник POST запиту
    data = request.json
    full_name = data.get("fullName")
    phone_number = data.get("phoneNumber")
    email = data.get("email")
    telegram_user = data.get("telegramUser", "Не вказано")

    message = (f"📩 Нова заявка на СТО\n\n"
               f"👤 Ім'я: {full_name}\n"
               f"📞 Телефон: {phone_number}\n"
               f"📧 Email: {email}\n"
               f"💬 Telegram: {telegram_user}")

    response = requests.post(TELEGRAM_API_URL, json={
        "chat_id": ADMIN_CHAT_ID,
        "text": message
    })

    if response.status_code == 200:
        return jsonify({"status": "success", "message": "Заявка надіслана!"})
    else:
        return jsonify({"status": "error", "message": "Помилка при надсиланні"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
