import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Завантажуємо змінні середовища з файлу .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

reminder_users = set()
scheduler = AsyncIOScheduler()

# Команда /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привіт! Я бот для запису на СТО.\n"
                         "📅 /reminder - увімкнути щомісячне нагадування\n"
                         "❌ /stopreminder - вимкнути нагадування\n"
                         "📞 /support - зв'язатися з підтримкою")

# Увімкнути нагадування
@dp.message(Command("reminder"))
async def enable_reminder(message: types.Message):
    reminder_users.add(message.from_user.id)
    await message.answer("✅ Ви підписалися на щомісячні нагадування про ТО.")

# Вимкнути нагадування
@dp.message(Command("stopreminder"))
async def disable_reminder(message: types.Message):
    reminder_users.discard(message.from_user.id)
    await message.answer("❌ Нагадування вимкнено.")

# Надсилання нагадувань раз на місяць
async def send_reminders():
    for user_id in reminder_users:
        try:
            await bot.send_message(user_id, "🔔 Нагадуємо про профілактику на СТО!")
        except:
            pass

# Підтримка
support_requests = {}

@dp.message(Command("support"))
async def request_support(message: types.Message):
    support_requests[message.from_user.id] = message.chat.id
    await bot.send_message(ADMIN_CHAT_ID, f"📩 Новий запит в підтримку від @{message.from_user.username}")
    await message.answer("✍️ Напишіть ваше питання. Адміністратор відповість вам.")

@dp.message(lambda message: message.from_user.id in support_requests)
async def forward_to_admin(message: types.Message):
    await bot.send_message(ADMIN_CHAT_ID, f"📨 Питання від @{message.from_user.username}: {message.text}")

@dp.message(F.chat.id == int(ADMIN_CHAT_ID))
async def reply_to_user(message: types.Message):
    if message.reply_to_message:
        user_id = next((uid for uid, chat in support_requests.items() if chat == message.chat.id), None)
        if user_id:
            await bot.send_message(user_id, f"📩 Відповідь від підтримки: {message.text}")

# Кнопка для адміністратора для відправки рекомендації всім
@dp.message(Command("send_recommendation"))
async def send_recommendation(message: types.Message):
    if message.from_user.id == int(ADMIN_CHAT_ID):  # Перевірка, чи це адмін
        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text="Надіслати рекомендацію", callback_data="send_reminder_to_all")
        keyboard.add(button)

        await message.answer("Натисніть кнопку, щоб надіслати рекомендацію всім користувачам:", reply_markup=keyboard)

@dp.callback_query(F.data == "send_reminder_to_all")
async def send_recommendation_to_all(call: types.CallbackQuery):
    if call.from_user.id == int(ADMIN_CHAT_ID):  # Перевірка, чи це адмін
        for user_id in reminder_users:
            try:
                await bot.send_message(user_id, "🔔 Не забувайте про профілактику на СТО! Вчасне обслуговування — запорука довговічності вашого авто.")
            except:
                pass

        await call.message.answer("✅ Рекомендацію надіслано всім підписникам.")
        await call.answer()

async def main():
    scheduler.add_job(send_reminders, "interval", weeks=4)
    scheduler.start()  # Перенесли запуск сюди
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
