from aiogram.filters import Command
from aiogram.types import Message

from weather import router
from weather.keyboards import request_location_kb
from weather.context import DialogueState


@router.message(Command("weather"))
async def cmd_weather(message: Message, ctx):
    """
    Начало диалога для сбора данных
    1. Начальный город, можно геолокацией <= ты здесь
    2. Конечный город, можно геолокацией
    3. Промежуточные остановки, если есть
    """
    markup = request_location_kb()
    markup.input_field_placeholder = "Введите начальную точку"

    ctx.set_dialogue(message.from_user.id, {"state": DialogueState.START_CITY})

    await message.answer("Блабла блы", reply_markup=markup)


@router.message(Command("ctx"))
async def cmd_ctx(message: Message, ctx):
    await message.answer(f"{ctx.dialogue=}")
