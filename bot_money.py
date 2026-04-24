import asyncio
import os
import aiosqlite
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

DB = "db.sqlite3"

PAY_LINK = "https://buy.stripe.com/test_XXXX"  # заміниш пізніше

async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            tg_id INTEGER UNIQUE,
            paid INTEGER DEFAULT 0
        )
        """)
        await db.commit()

def keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатити доступ", url=PAY_LINK)],
        [InlineKeyboardButton(text="✅ Я оплатив", callback_data="paid")]
    ])

@dp.message(F.text == "/start")
async def start(m: Message):
    async with aiosqlite.connect(DB) as db:
        await db.execute("INSERT OR IGNORE INTO users (tg_id) VALUES (?)", (m.from_user.id,))
        await db.commit()

    await m.answer("🔒 NEXARA ACCESS", reply_markup=keyboard())

@dp.callback_query(F.data == "paid")
async def paid(c):
    async with aiosqlite.connect(DB) as db:
        await db.execute("UPDATE users SET paid=1 WHERE tg_id=?", (c.from_user.id,))
        await db.commit()

    await c.message.answer("✅ PRO ACCESS ACTIVE")

@dp.message()
async def handler(m: Message):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute("SELECT paid FROM users WHERE tg_id=?", (m.from_user.id,))
        row = await cur.fetchone()

    if row and row[0] == 1:
        await m.answer("⚙️ PRO MODE ACTIVE")
    else:
        await m.answer("🔒 NO ACCESS")

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
