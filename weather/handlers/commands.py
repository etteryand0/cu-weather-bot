from aiogram.filters import Command
from aiogram.types import Message

from weather import router
from keyboards import request_location_kb


@router.message(Command("weather"))
async def cmd_weather(message: Message):
    """
    Начало диалога для сбора данных
    1. Начальный город, можно геолокацией <= ты здесь
    2. Конечный город, можно геолокацией
    3. Промежуточные остановки, если есть
    """
    markup = request_location_kb()
    markup.input_field_placeholder = "Введите начальную точку"

    await message.answer("Блабла блы", reply_markup=markup)
