import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from aiohttp import web
import os

# Твой токен бота
BOT_TOKEN = "YOUR_BOT_TOKEN"
WEBHOOK_HOST = "https://telegram-gpt-bot-hwnk.onrender.com"  # Замени на свой Render URL!
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# Настройки сервера
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 8000))

# Создаём бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Логирование
logging.basicConfig(level=logging.INFO)

# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.reply("Привет! Я работаю через Webhook.")

# Функция при старте
async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL)
    print(f"Webhook установлен: {WEBHOOK_URL}")

# Функция при выключении
async def on_shutdown(dispatcher):
    await bot.delete_webhook()

# Запускаем webhook-сервер
if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
