from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

button = [
[types.KeyboardButton(text='🏠 Return to main page')]
]
keyboard = types.ReplyKeyboardMarkup(keyboard=button,
                                    resize_keyboard=True,
                                    one_time_keyboard=False,
                                    input_field_placeholder='Talk to me...')