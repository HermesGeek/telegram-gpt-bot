import os
import aiohttp
import asyncio
from aiogram import Bot, Dispatcher, types

# Замените YOUR_TELEGRAM_BOT_TOKEN на настоящий токен или установите переменную окружения TELEGRAM_BOT_TOKEN.
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7952421114:AAH6aaqUxWpFpU70yZazgVuchDI9hHKmGfI")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для отправки запроса на ChatGPT и получения ответа
async def ask_chatgpt(prompt: str) -> str:
    url = "https://chatgpt.com/g/g-67b9c92040e48191a87443fda19625ea-gikbot"
    payload = {"prompt": prompt}  # Данные для запроса
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("response", "Ответ не найден.")
                else:
                    return f"Ошибка: сервер вернул статус {response.status}"
    except Exception as e:
        return f"Произошла ошибка: {e}"

# Обработчик входящих сообщений
@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text
    await message.reply("Подождите, обрабатываю ваш запрос...")
    answer = await ask_chatgpt(user_text)
    await message.reply(answer)

# Функция для запуска бота в режиме polling
async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
