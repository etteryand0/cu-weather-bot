import logging

import aiohttp
import asyncio
from aiogram import F
from aiogram.types import Message, ReplyKeyboardRemove

from weather_bot.api import get_location_key_by_city, parse_error_code
from weather_bot.context import Context
from weather_bot.filters import DialogueStateFilter
from weather_bot.weather import router
from weather_bot.weather.context import DialogueState, save_end_city, save_start_city


@router.message(
    F.text, DialogueStateFilter([DialogueState.START_CITY, DialogueState.END_CITY])
)
async def msg_start_end_city(message: Message, ctx: Context):
    error_message = None
    try:
        location_key, city_name = await get_location_key_by_city(message.text)
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
            "Сервис погоды не распознал город, может вы ошиблись? Попробуйте снова",
            reply_markup=ReplyKeyboardRemove(),
        )
        return

    dialogue = ctx.get_dialogue(message.from_user.id)
    if dialogue.state == DialogueState.START_CITY:
        await save_start_city(message, dialogue, location_key, city_name)
        return

    await save_end_city(message, dialogue, location_key, city_name)


@router.message(F.text, DialogueStateFilter(DialogueState.PITSTOP_CITIES))
async def msg_pitstop_cities(message: Message, ctx: Context):
    if message.text == "Нет промежуточных точек":
        # Приступить к предсказанию погоды
        return

    pitstop_cities = list(
        filter(
            lambda city: len(city) > 3,
            [city.strip() for city in message.text.split(",")],
        )
    )

    async with aiohttp.ClientSession() as session:
        coroutines = [
            get_location_key_by_city(city, session=session) for city in pitstop_cities
        ]

        error_message = None
        try:
            results = await asyncio.gather(*coroutines)
        except (ConnectionError, TimeoutError) as e:
            logging.error(e)
            error_message = "Сервис погоды не доступен в данный момент"
        except aiohttp.ClientResponseError as e:
            logging.error(e)
            error_message = parse_error_code(e.status)

        if error_message is not None:
            await message.answer(error_message)
            return

    missing_cities = []
    for i, data in enumerate(results):
        if data[0] is None:
            missing_cities.append(pitstop_cities[i])

    await message.answer(f"{ctx.get_dialogue(message.from_user.id)}")
    await message.answer(f"pitstop_cities: {",".join(pitstop_cities)}")

    if len(missing_cities) == 1:
        await message.answer(
            f"Сервис погоды не смог распознать город {missing_cities[0]}. Пожалуйста, повторите попытку"
        )
        return
    elif len(missing_cities) > 1:
        await message.answer(
            f"Сервис погоды не смог распознать города {', '.join(missing_cities)}. Пожалуйста, повторите попытку"
        )
        return

    # Вот здесь уже погоду предсказываем и показываем графики
