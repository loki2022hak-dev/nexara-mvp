import asyncio
import os
from aiogram import Bot, Dispatcher

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN missing")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    print("BOT STARTING OK")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
