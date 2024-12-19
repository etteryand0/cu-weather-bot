from aiogram import F
from aiogram.types import Message

from weather import router


@router.message(F.location)
async def location_handler(message: Message):
    lat, lon = message.location.latitude, message.location.longitude
    await message.reply(f"{lat=}, {lon=}")
