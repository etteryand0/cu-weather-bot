import os

import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from . import weather
from . import info
from weather_bot.context import Context

logging.basicConfig(level=logging.INFO)
load_dotenv()


async def main():
    if os.environ.get("BOT_TOKEN") is None:
        raise Exception("Токена бота 'BOT_TOKEN' не существует в окружении")

    bot = Bot(token=os.environ.get("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_routers(weather.router, info.router)

    ctx = Context()
    await dp.start_polling(bot, ctx=ctx)


if __name__ == "__main__":
    asyncio.run(main())
