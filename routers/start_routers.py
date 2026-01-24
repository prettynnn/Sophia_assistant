from aiogram.filters import Command
from aiogram.enums import ChatAction
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramConflictError, TelegramBadRequest

from database.db import connector_to_server, select_data_from_table, include_in_table
from keyboards.inline_keyboards import inline_keyboard
from others.stickers import stickers
from database.roles import system
from others.states import User
from others.cfg import log

import random

start_router = Router()

@start_router.message(Command("start", prefix='/!'))
async def start_handler(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    stick_id = random.choice(stickers)
    
    try:
        connect = await connector_to_server()
        data = await select_data_from_table(connect, 
                                            user_id)
        if user_id not in data:
            content = 'I am a helpful assistant a Sophia'
            await include_in_table(connect,
                                   user_id,
                                   system,
                                   content)
            await message.bot.send_chat_action(action=ChatAction.TYPING,
                                               chat_id=message.chat.id)
            await message.answer_sticker(sticker=stick_id)
            await message.answer(text='💬 Select language',
                                 reply_markup=inline_keyboard)
            await state.set_state(User.language)
        else:
            await message.bot.send_chat_action(action=ChatAction.TYPING,
                                                chat_id=message.chat.id)
            await message.answer_sticker(sticker=stick_id)
            await message.answer(text='💬 Select language',
                                 reply_markup=inline_keyboard)
    except TelegramConflictError as a:
        log(f'This bot launched somewhere else! - {a}')
    except TelegramBadRequest as b:
        log(f'Request was declined a Telegram! - {b}')
