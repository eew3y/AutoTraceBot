import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types

# Отримуємо токен з Environment Variables на Vercel
TOKEN = os.getenv("BOT_TOKEN")

# Ініціалізація бота, диспетчера та FastAPI додатку
bot = Bot(token=TOKEN)
dp = Dispatcher()
app = FastAPI()


# Базовий хендлер для Ехо-бота
@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(message.text)


# Ендпоінт, на який Telegram буде надсилати оновлення (Webhook)
@app.post("/api/webhook")
async def webhook_endpoint(request: Request):
    # Отримуємо JSON від Telegram
    update_data = await request.json()

    # Конвертуємо JSON у об'єкт Update (синтаксис aiogram 3.x)
    update = types.Update.model_validate(update_data, context={"bot": bot})

    # Передаємо оновлення в диспетчер
    await dp.feed_update(bot, update)

    # Повертаємо 200 OK, щоб Telegram зрозумів, що ми отримали повідомлення
    return {"status": "ok"}
