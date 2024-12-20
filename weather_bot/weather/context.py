from aiogram.types import Message

from weather_bot.weather.keyboards import request_location_kb, deny_pitstop_kb
from weather_bot.context import Dialogue


class DialogueState:
    """
    enum для стейтов диалога weather
    """

    START_CITY = "start_city"
    END_CITY = "end_city"
    PITSTOP_CITIES = "pitstop_cities"


async def save_start_city(
    message: Message, dialogue: Dialogue, location_key: str, city_name: str
):
    dialogue.set_state(DialogueState.END_CITY)
    dialogue.set_data({"start_city": {"key": location_key, "name": city_name}})

    markup = request_location_kb()
    markup.input_field_placeholder = "Введите конечную точку"
    await message.answer(
        f"Отлично! Я зафиксировал ваш начальный город: {city_name}. 🌆 Теперь, чтобы продолжить, пожалуйста, укажите конечный город, в который вы собираетесь поехать. Жду вашего ответа!",
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
        f"Отлично! Ваш конечный город: {city_name}. 🌟 Теперь, пожалуйста, укажите промежуточные города, если они есть. Просто отправьте их через запятую в одном сообщении. Жду вашего ответа!",
        reply_markup=markup,
    )
