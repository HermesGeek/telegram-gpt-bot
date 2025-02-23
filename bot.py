import os
import aiohttp
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiohttp import web

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Максимальная длина сообщения Telegram (с запасом)
MAX_MESSAGE_LENGTH = 4096

# Получаем токен бота (замените на настоящий токен или задайте переменную окружения)
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7952421114:AAH6aaqUxWpFpU70yZazgVuchDI9hHKmGfI")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для отправки запроса на API и получения ответа
async def ask_chatgpt(prompt: str) -> str:
    url = "https://chatgpt.com/g/g-67b9c92040e48191a87443fda19625ea-gikbot"
    payload = {"prompt": prompt}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=payload) as response:
                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    data = await response.json()
                    return data.get("response", "Ответ не найден.")
                else:
                    # Если ответ не в формате JSON, возвращаем текст
                    text = await response.text()
                    return text.strip()
    except Exception as e:
        return f"Произошла ошибка: {e}"

# Обработчик входящих сообщений от пользователей Telegram
@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text
    try:
        await message.reply("Подождите, обрабатываю ваш запрос...")
    except TelegramForbiddenError:
        pass

    answer = await ask_chatgpt(user_text)
    logging.info("Ответ от API: %s", answer)
    if len(answer) > MAX_MESSAGE_LENGTH:
        answer = answer[:MAX_MESSAGE_LENGTH - 50] + "\n\n[Обрезано, ответ слишком длинный]"
    try:
        await message.reply(answer)
    except TelegramForbiddenError:
        pass
    except TelegramBadRequest as bad_req:
        logging.error("TelegramBadRequest: %s", bad_req)

# Настройка webhook: формируем путь и URL для приема обновлений
WEBHOOK_PATH = f"/webhook/{TOKEN}"
DOMAIN = os.environ.get("RENDER_EXTERNAL_URL", "https://telegram-gpt-bot-hwnk.onrender.com")
WEBHOOK_URL = DOMAIN + WEBHOOK_PATH

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info("Webhook установлен: %s", WEBHOOK_URL)

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

# Обработчик POST-запросов от Telegram (webhook)
async def handle_webhook(request: web.Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return web.Response(text="OK")

# Обработчик GET-запросов для корневого URL (приветственное сообщение)
async def handle_root(request: web.Request):
    return web.Response(text="Привет! Это сервис Telegram-бота. Для общения используйте Telegram.")

def main():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)
    app.router.add_get("/", handle_root)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
