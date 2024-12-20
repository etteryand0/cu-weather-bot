import os

import aiohttp


async def get_location_key_by_location(lat, lon, *, session=None):
    url = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"
    params = {"apikey": os.environ["ACCUWEATHER_API_KEY"], "q": f"{lat},{lon}"}

    if session is not None:
        response = await session.get(url, params=params)
        response.raise_for_status()
        data = await response.json()
    else:
        async with aiohttp.ClientSession() as s:
            response = await s.get(url, params=params)
            response.raise_for_status()
            data = await response.json()
    if data:
        return data["Key"]
    return None


async def get_location_key_by_city(city_name, *, session=None):
    url = "http://dataservice.accuweather.com/locations/v1/cities/search"
    params = {"apikey": os.environ["ACCUWEATHER_API_KEY"], "q": city_name}

    if session is not None:
        response = await session.get(url, params=params)
        response.raise_for_status()
        data = await response.json()
    else:
        async with aiohttp.ClientSession() as s:
            response = await s.get(url, params=params)
            response.raise_for_status()
            data = await response.json()
    if data:
        return data[0]["Key"]
    return None


async def get_weather_data(location_key, *, session=None):
    url = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}"
    params = {
        "apikey": os.environ["ACCUWEATHER_API_KEY"],
        "details": "true",
        "metric": "true",
    }
    if session is not None:
        response = await session.get(url, params=params)
        response.raise_for_status()
        return await response.json()

    async with aiohttp.ClientSession() as s:
        response = await s.get(url, params=params)
        response.raise_for_status()
        return await response.json()


def parse_error_code(status_code):
    match status_code:
        case 400:
            return "Сервис погоды получил некорректные данные"
        case 401:
            return "Сервис погоды не распознал API ключ нашего веб-приложения"
        case 403:
            return "Превышен лимит запросов сервиса погоды"
        case _:
            return "Сервис погоды не доступен в данный момент"
