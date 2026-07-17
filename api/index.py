import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Update
from mangum import Mangum

# Ініціалізація бота та диспетчера
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Створюємо додаток FastAPI
app = FastAPI()


# Хендлер на команду /start
@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer("Привіт! Тепер усе точно працює через Mangum на Vercel! 🚀")


# Хендлер ехо
@dp.message()
async def echo_message(message: types.Message):
    if message.text:
        await message.answer(message.text)


# Головний маршрут для перевірки в браузері
@app.get("/")
async def root():
    return {"status": "working", "bot": "active"}


# Маршрут для прийому вебхуків від Telegram
@app.post("/")
async def telegram_webhook(request: Request):
    try:
        json_data = await request.json()
        update = Update.model_validate(json_data, context={"bot": bot})
        await dp.feed_update(bot, update)
    except Exception as e:
        print(f"Error processing update: {e}")

    return {"ok": True}


# Створюємо handler для Vercel Serverless
handler = Mangum(app)
