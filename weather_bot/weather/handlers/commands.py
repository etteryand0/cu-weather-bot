from aiogram.filters import Command
from aiogram.types import Message

from weather_bot.context import Context
from weather_bot.weather import router
from weather_bot.weather.keyboards import request_location_kb
from weather_bot.weather.context import DialogueState


start_msg = """Отлично! Давайте начнем. 🌍

Я помогу вам получить прогноз погоды для вашего маршрута. Пожалуйста, укажите начальный город, с которого вы планируете отправиться. После этого мы сможем добавить конечный город и промежуточные точки. Жду вашего ответа!
"""


@router.message(Command("weather"))
async def cmd_weather(message: Message, ctx: Context):
    """
    Начало диалога для сбора данных
    1. Начальный город, можно геолокацией <= ты здесь
    2. Конечный город, можно геолокацией
    3. Промежуточные остановки, если есть
    4. Срок прогнозирования (1 или 5 дней)
    5. Результат - прогнозы по маршруту
    """
    markup = request_location_kb()
    markup.input_field_placeholder = "Введите начальную точку"

    ctx.start_dialogue(message.from_user.id, DialogueState.START_CITY)

    await message.answer(start_msg, reply_markup=markup)
