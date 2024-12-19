from aiogram.filters import Command
from aiogram.types import Message

from weather_bot.context import Context
from weather_bot.weather import router
from weather_bot.weather.keyboards import request_location_kb
from weather_bot.weather.context import DialogueState


@router.message(Command("weather"))
async def cmd_weather(message: Message, ctx: Context):
    """
    Начало диалога для сбора данных
    1. Начальный город, можно геолокацией <= ты здесь
    2. Конечный город, можно геолокацией
    3. Промежуточные остановки, если есть
    """
    markup = request_location_kb()
    markup.input_field_placeholder = "Введите начальную точку"

    ctx.start_dialogue(message.from_user.id, DialogueState.START_CITY)

    await message.answer("Блабла блы", reply_markup=markup)


@router.message(Command("ctx"))
async def cmd_ctx(message: Message, ctx: Context):
    await message.answer(f"{ctx.get_dialogue(message.from_user.id)}")
