from aiogram import types

button = [
[types.KeyboardButton(text='🏠 Return to main page'),
 types.KeyboardButton(text='🌏 Change language')]
]
reply_keyboard = types.ReplyKeyboardMarkup(keyboard=button,
                                    resize_keyboard=True,
                                    one_time_keyboard=False,
                                    input_field_placeholder='Talk to me...')