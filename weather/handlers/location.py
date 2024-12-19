from aiogram import F
from aiogram.types import Message

from weather import router
from weather.context import DialogueState


@router.message(F.location)
async def location_handler(message: Message, ctx):
    dialogue = ctx.get_dialogue(message.from_user.id)

    if not dialogue:
        # Игнорируем локацию без статуса диалога
        return

    lat, lon = message.location.latitude, message.location.longitude

    match dialogue["state"]:
        case DialogueState.START_CITY:
            dialogue["state"] = DialogueState.END_CITY
            dialogue["data"] = {"start_city": [lat, lon]}
            ctx.set_dialogue(message.from_user.id, dialogue)
            return
        case DialogueState.END_CITY:
            dialogue["state"] = DialogueState.PITSTOP_CITIES
            dialogue["data"]["end_city"] = [lat, lon]
            ctx.set_dialogue(message.from_user.id, dialogue)
            return

    await message.reply(f"{lat=}, {lon=}")
