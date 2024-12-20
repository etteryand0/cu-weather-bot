import logging
import aiohttp

from aiogram import F
from aiogram.types import Message, ReplyKeyboardRemove
import aiohttp.http_exceptions

from weather_bot.filters import DialogueStateFilter
from weather_bot.weather import router
from weather_bot.weather.context import DialogueState
from weather_bot.context import Context
from weather_bot.api import get_location_key_by_location, parse_error_code

from . import save_end_city, save_start_city


@router.message(
    F.location, DialogueStateFilter([DialogueState.START_CITY, DialogueState.END_CITY])
)
async def location_handler(message: Message, ctx: Context):
    lat, lon = message.location.latitude, message.location.longitude
    error_message = None

    try:
        location_key, city_name = await get_location_key_by_location(lat, lon)
    except (ConnectionError, TimeoutError) as e:
        logging.error(e)
        error_message = "Сервис погоды не доступен в данный момент"
    except aiohttp.ClientResponseError as e:
        logging.error(e)
        error_message = parse_error_code(e.status)

    if error_message is not None:
        await message.answer(error_message)
        return

    if location_key is None:
        await message.answer(
            "Сервис погоды не смог установить ваше местоположение, пожалуйста, напишите название города",
            reply_markup=ReplyKeyboardRemove(),
        )

    dialogue = ctx.get_dialogue(message.from_user.id)

    if dialogue.state == DialogueState.START_CITY:
        await save_start_city(message, dialogue, location_key, city_name)
        return

    await save_end_city(message, dialogue, location_key, city_name)
