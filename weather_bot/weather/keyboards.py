from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def request_location_kb() -> ReplyKeyboardMarkup:
    keyboard = KeyboardButton(text="📍 Текущее местоположение", request_location=True)
    markup = ReplyKeyboardMarkup(
        keyboard=[[keyboard]],
        resize_keyboard=True,
        one_time_keyboard=True,
        is_persistent=True,
    )
    return markup


def deny_pitstop_kb() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Нет промежуточных точек")]],
        resize_keyboard=True,
        one_time_keyboard=True,
        is_persistent=True,
    )
    return markup


def forecast_days_kb() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text="1 день"),
            KeyboardButton(text="5 дней"),
        ]
    ]
    markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
        is_persistent=True,
    )
    return markup
