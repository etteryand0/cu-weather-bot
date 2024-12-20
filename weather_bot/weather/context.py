from aiogram.types import Message

from weather_bot.weather.keyboards import (
    request_location_kb,
    deny_pitstop_kb,
    forecast_days_kb,
)
from weather_bot.context import Dialogue


class DialogueState:
    """
    enum для стейтов диалога weather
    """

    START_CITY = "start_city"
    END_CITY = "end_city"
    PITSTOP_CITIES = "pitstop_cities"
    FORECAST_DAYS = "forecast_days"


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


async def save_pitstop_cities(
    message: Message, dialogue: Dialogue, pitstop_cities: list[tuple[str, str]]
):
    if len(pitstop_cities) == 0:
        return

    d = dialogue.data
    d["pitstop_cities"] = pitstop_cities
    dialogue.set_state(DialogueState.FORECAST_DAYS)
    dialogue.set_data(d)

    msg = f"Отлично! 🎉 Теперь выберите, на какой срок вы хотите получить прогноз погоды: 1, 5 или 10 дней. Пожалуйста, нажмите на соответствующую кнопку, чтобы сделать свой выбор!"
    if len(pitstop_cities) > 1:
        msg = f"Отлично! Я зафиксировал промежуточные точки. 🎉 Теперь выберите, на какой срок вы хотите получить прогноз погоды: 1, 5 или 10 дней. Пожалуйста, нажмите на соответствующую кнопку, чтобы сделать свой выбор!"

    markup = forecast_days_kb()
    await message.answer(msg, reply_markup=markup)
