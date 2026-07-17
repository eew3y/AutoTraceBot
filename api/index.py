import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Update

# Ініціалізація бота (токен беремо зі змінних оточення)
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()


# Хендлер на команду /start
@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer(
        "Привіт! Я простіший Ехо-бот на вебхуках, запущений на Vercel!"
    )


# Хендлер ехо (повертає текст назад)
@dp.message()
async def echo_message(message: types.Message):
    if message.text:
        await message.answer(message.text)


# Головна асинхронна функція для Vercel (серверна частина)
async def handler(request):
    if request.method == "POST":
        try:
            # Отримуємо JSON від Telegram
            json_string = await request.text()
            update = Update.model_validate_json(json_string)

            # Передаємо апдейт в диспетчер aiogram
            await dp.feed_update(bot, update)
        except Exception as e:
            print(f"Error processing update: {e}")

    # Завжди повертаємо 200 OK для Telegram
    return {"statusCode": 200, "headers": {"Content-Type": "text/plain"}, "body": "OK"}


# Точка входу для Vercel Serverless (WSGI адаптер)
def app(environ, start_response):
    # Створюємо простий об'єкт реквесту для асинхронного обробника
    class RequestMock:
        method = environ.get("REQUEST_METHOD", "GET")

        async def text(self):
            try:
                request_body_size = int(environ.get("CONTENT_LENGTH", 0))
                return environ["wsgi.input"].read(request_body_size).decode("utf-8")
            except:
                return ""

    loop = asyncio.get_event_loop()
    response = loop.run_until_complete(handler(RequestMock()))

    start_response(
        f"{response['statusCode']} OK", [(k, v) for k, v in response["headers"].items()]
    )
    return [response["body"].encode("utf-8")]
