from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def request_location_kb() -> ReplyKeyboardMarkup:
    keyboard = KeyboardButton(text="📍 Текущее местоположение", request_location=True)
    markup = ReplyKeyboardMarkup(keyboard=[[keyboard]], resize_keyboard=True)
    return markup
