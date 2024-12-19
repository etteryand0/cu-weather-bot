from aiogram import F
from aiogram.types import Message

from weather_bot.weather import router
from weather_bot.weather.context import DialogueState
from weather_bot.context import Context


@router.message(F.location)
async def location_handler(message: Message, ctx: Context):
    dialogue = ctx.get_dialogue(message.from_user.id)

    if not dialogue:
        # Игнорируем локацию без статуса диалога
        return

    lat, lon = message.location.latitude, message.location.longitude

    match dialogue.state:
        case DialogueState.START_CITY:
            dialogue.set_state(DialogueState.END_CITY)
            dialogue.set_data({"start_city": [lat, lon]})
            return
        case DialogueState.END_CITY:
            d = dialogue.data
            d["end_city"] = [lat, lon]
            dialogue.set_state(DialogueState.PITSTOP_CITIES)
            dialogue.set_data(d)
            ctx.set_dialogue(message.from_user.id, dialogue)
            return

    await message.reply(f"{lat=}, {lon=}")
