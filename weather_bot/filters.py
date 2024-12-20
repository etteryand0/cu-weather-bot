from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message

from weather_bot.context import Context


class DialogueStateFilter(BaseFilter):
    """
    Фильтр для хэндлеров aiogram по статусу диалога
    """

    def __init__(self, state: Union[str, list[str]]):
        self.state = state

    async def __call__(self, message: Message, ctx: Context) -> bool:
        dialogue = ctx.get_dialogue(message.from_user.id)
        if dialogue is None:
            return False

        if isinstance(self.state, list):
            return dialogue.state in self.state

        return dialogue.state == self.state
