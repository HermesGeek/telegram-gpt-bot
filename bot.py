import os
import aiohttp
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiohttp import web

# Получаем токен бота (убедитесь, что он правильный)
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "7952421114:AAH6aaqUxWpFpU70yZazgVuchDI9hHKmGfI")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для отправки запроса на ChatGPT и получения ответа
async def ask_chatgpt(prompt: str) -> str:
    url = "https://chatgpt.com/g/g-67b9c92040e48191a87443fda19625ea-gikbot"
    payload = {"prompt": prompt}  # Отправляем данные с ключом "prompt"
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

# Настройка webhook
WEBHOOK_PATH = f"/webhook/{TOKEN}"
# Укажите правильный домен вашего приложения на Render (например, https://your-app-name.onrender.com)
DOMAIN = os.environ.get("RENDER_EXTERNAL_URL", "https://telegram-gpt-bot-hwnk.onrender.com")
WEBHOOK_URL = DOMAIN + WEBHOOK_PATH

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info("Webhook установлен: %s", WEBHOOK_URL)

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

# Обработчик запросов от Telegram (webhook)
async def handle_webhook(request: web.Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.process_update(update)  # Изменено с feed_update на process_update
    return web.Response(text="OK")

def main():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
