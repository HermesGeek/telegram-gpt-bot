import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import openai
from dotenv import load_dotenv
import asyncio

# Загружаем переменные окружения из .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Настраиваем OpenAI API
openai.api_key = OPENAI_API_KEY

# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Я ГикБот 🤖 Задавай вопросы!")

# Обработчик сообщений
@dp.message()
async def chat_with_gpt(message: types.Message):
    try:
        response = openai.ChatCompletion.create(  # ✅ Правильный вызов API
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}],
        )
        reply = response["choices"][0]["message"]["content"]
        await message.answer(reply)

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer("Ошибка при запросе к OpenAI 😢")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
