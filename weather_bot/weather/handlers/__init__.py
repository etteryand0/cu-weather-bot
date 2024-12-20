from aiogram.types import Message

from weather_bot.weather.keyboards import request_location_kb, deny_pitstop_kb
from weather_bot.context import Dialogue
from weather_bot.weather.context import DialogueState


async def save_start_city(
    message: Message, dialogue: Dialogue, location_key: str, city_name: str
):
    dialogue.set_state(DialogueState.END_CITY)
    dialogue.set_data({"start_city": {"key": location_key, "name": city_name}})

    markup = request_location_kb()
    markup.input_field_placeholder = "Введите конечную точку"
    await message.answer(
        f"Начальный город: {city_name}. Теперь укажите конечный город.",
        reply_markup=markup,
    )


async def save_end_city(
    message: Message, dialogue: Dialogue, location_key: str, city_name: str
):
    d = dialogue.data
    d["end_city"] = {"key": location_key, "name": city_name}
    dialogue.set_state(DialogueState.PITSTOP_CITIES)
    dialogue.set_data(d)

    markup = deny_pitstop_kb()
    await message.answer(
        f"Конечный город: {city_name}. Осталось только указать промежуточные точки. Введите их через запятую",
        reply_markup=markup,
    )


from . import commands
from . import message
from . import location
