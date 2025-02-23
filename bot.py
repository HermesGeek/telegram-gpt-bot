import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
# URL, по которому Telegram будет отправлять обновления (замените на ваш URL на Render)
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"https://your-app-name.onrender.com{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Регистрируем хэндлеры, например:
@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Вы сказали: {message.text}")

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    print("Webhook установлен")

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()
    print("Webhook удалён")

async def handle_webhook(request: web.Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(update)
    return web.Response()

def main():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    
    # Render задаёт порт через переменную окружения PORT
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    asyncio.run(main())
