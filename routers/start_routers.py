from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ChatAction
from aiogram import types, Router, Bot
from aiogram.fsm.context import FSMContext

from keyboards.inline_keyboards import inline_keyboard
from database.memory import connector_to_server, select_data_from_table, include_in_table
from tokens import api_key
from others.stickers import stickers
from others.states import User

import random

bot = Bot(token=api_key)
start_router = Router()

@start_router.message(Command("start", prefix='/'))
async def start_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    chat_id = message.chat.id
    stick_id = random.choice(stickers)
    role = None
    content = None
    # language_text = '💬 Select language'
        
    connect = await connector_to_server()
    data = await select_data_from_table(connect, 
                                        user_id,
                                        role,
                                        content)
    
    if user_id not in data:
        role = 'system'
        content = 'I a helpful assistant a Sophia'
        await include_in_table(connect,
                               user_id,
                               role,
                               content)
        await message.bot.send_chat_action(action=ChatAction.TYPING,
                                           chat_id=chat_id)
        await message.answer(text='💬 Select language',
                            reply_markup=inline_keyboard)
        await state.set_state(User.language)
    else:
        await message.bot.send_chat_action(action=ChatAction.TYPING,
                                           chat_id=chat_id)
        await message.answer_sticker(sticker=stick_id)
        await message.answer(text='💬 Select language',
                            reply_markup=inline_keyboard)
