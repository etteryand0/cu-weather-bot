import logging

import aiohttp
import asyncio
from aiogram import F
from aiogram.types import Message, ReplyKeyboardRemove

from weather_bot.api import (
    get_location_key_by_city,
    parse_error_code,
    get_forecast,
    parse_weather_conditions,
)
from weather_bot.context import Context
from weather_bot.filters import DialogueStateFilter
from weather_bot.weather import router
from weather_bot.weather.keyboards import forecast_days_kb
from weather_bot.weather.context import (
    DialogueState,
    save_end_city,
    save_start_city,
    save_pitstop_cities,
)


@router.message(
    F.text, DialogueStateFilter([DialogueState.START_CITY, DialogueState.END_CITY])
)
async def msg_start_end_city(message: Message, ctx: Context):
    """
    Данный хэндлер получает сообщением название города: начального или конечного,
    отправляет запрос в сервис погоды для получения location_key и сохраняет
    в глобальный контекст название города и location_key. В зависимости от
    состояния диалога даёт пользователю следующие инструкции
    """
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
            "К сожалению, я не смог распознать город. 😕 Возможно, где-то была опечатка. Пожалуйста, попробуйте еще раз. Жду вашего ответа!",
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
    """
    Данный хэндлер получает сообщением названия промежуточных городов,
    отправляет множество запросов в сервис погоды для получения location_key
    и сохраняет в глобальный контекст названия и location_key промежуточных городов.
    В коцне просит у пользователя срок прогнозирования погоды.
    """
    dialogue = ctx.get_dialogue(message.from_user.id)

    if message.text == "Нет промежуточных точек":
        markup = forecast_days_kb()
        dialogue.set_state(DialogueState.FORECAST_DAYS)
        await message.answer(
            "Выберите, на какой срок вы хотите получить прогноз погоды: 1, 5 или 10 дней. Пожалуйста, нажмите на соответствующую кнопку, чтобы сделать свой выбор!",
            reply_markup=markup,
        )
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

    if len(missing_cities) == 1:
        await message.answer(
            f"К сожалению, я не смог распознать город {missing_cities[0]}. 😕 Возможно, где-то была опечатка. Пожалуйста, попробуйте еще раз и укажите промежуточные города через запятую в одном сообщении. Жду вашего ответа!"
        )
        return
    elif len(missing_cities) > 1:
        await message.answer(
            f"К сожалению, я не смог распознать города {', '.join(missing_cities)}. 😕 Возможно, где-то была опечатка. Пожалуйста, попробуйте еще раз и укажите промежуточные города через запятую в одном сообщении. Жду вашего ответа!"
        )
        return

    await save_pitstop_cities(message, dialogue, results)


@router.message(
    F.text.in_({"1 день", "5 дней"}),
    DialogueStateFilter(DialogueState.FORECAST_DAYS),
)
async def msg_forecast_days(message: Message, ctx: Context):
    """
    Данный хэндлер получает срок прогнозирования и обращается в сервис погоды.
    Получив прогнозы, отправляет их пользователю отдельными сообщениями -
    1 город = 1 сообщение
    """
    dialogue = ctx.get_dialogue(message.from_user.id)
    days_to_forecast = 1
    if message.text == "5 дней":
        days_to_forecast = 5

    location_keys = (
        []
        if dialogue.data.get("pitstop_cities") is None
        else [key for (key, _) in dialogue.data["pitstop_cities"]]
    )
    location_keys.insert(0, dialogue.data["start_city"]["key"])
    location_keys.append(dialogue.data["end_city"]["key"])

    async with aiohttp.ClientSession() as session:
        coroutines = [
            get_forecast(key, days_to_forecast, session=session)
            for key in location_keys
        ]

        error_message = None
        try:
            city_forecasts = await asyncio.gather(*coroutines)
        except (ConnectionError, TimeoutError) as e:
            logging.error(e)
            error_message = "Сервис погоды не доступен в данный момент"
        except aiohttp.ClientResponseError as e:
            logging.error(e)
            error_message = parse_error_code(e.status)

        if error_message is not None:
            await message.answer(error_message)
            return

    city_names = (
        []
        if dialogue.data.get("pitstop_cities") is None
        else [name for (_, name) in dialogue.data["pitstop_cities"]]
    )
    city_names.insert(0, dialogue.data["start_city"]["name"])
    city_names.append(dialogue.data["end_city"]["name"])

    await message.answer(
        "Отлично! Вот прогноз погоды для вашего маршрута",
        reply_markup=ReplyKeyboardRemove(),
    )

    for i, forecast in enumerate(city_forecasts):
        msg = f"Город: {city_names[i]}"
        for day, daily_forecast in enumerate(forecast["DailyForecasts"], start=1):
            data = parse_weather_conditions(daily_forecast)
            msg += f"\nДень {day}, {data["date"]}:"
            msg += f"""
🌞 Дневная температура: {data["day_temperature"]}°C
🌙 Ночная температура: {data["night_temperature"]}°C
💨 Скорость ветра: {data["wind_speed"]} км/ч
🌧️ Вероятность осадков: {data["precipitation_probability"]}
💧 Влажность: {data["humidity"]}%\n"""

        await message.answer(msg)

    ctx.end_dialogue(message.from_user.id)
