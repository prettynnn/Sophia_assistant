from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_en = InlineKeyboardButton(text='🇺🇸 English', callback_data='lang_en')
button_ru = InlineKeyboardButton(text='🇷🇺 Русский', callback_data='lang_ru')
button_zh = InlineKeyboardButton(text='🇨🇳 中國人', callback_data='lang_zh')
button_jp = InlineKeyboardButton(text='🇯🇵 日本語', callback_data='lang_jp')

inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[button_en, 
                      button_zh],
                     [button_jp, 
                      button_ru]
                     ])
