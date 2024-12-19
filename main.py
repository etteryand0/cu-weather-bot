import os

import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command


load_dotenv()

if os.environ.get("BOT_TOKEN") is None:
    raise Exception("Токена бота 'BOT_TOKEN' не существует в окружении")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.environ.get("BOT_TOKEN"))
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
