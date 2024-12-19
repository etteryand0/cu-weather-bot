from aiogram.filters import Command
from aiogram.types import Message

from info import router, start_message, help_message


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(start_message)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(help_message)
