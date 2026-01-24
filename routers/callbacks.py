from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from others import greetings
from others.states import User
from keyboards.reply_keyboards import reply_keyboard

callback_router = Router()

@callback_router.callback_query(User.language)
async def select_language(callback: CallbackQuery, state: FSMContext) -> None:   
    if callback.data == 'lang_en':
        await state.clear()
        await state.update_data(user=greetings.en)
        await callback.message.delete()
        await callback.message.answer(text=greetings.en,
                                      reply_markup=reply_keyboard)
        await state.set_state(None)
    elif callback.data == 'lang_ru':
        await state.clear()
        await state.update_data(user=greetings.ru)
        await callback.message.delete()
        await callback.message.answer(text=greetings.ru,
                                      reply_markup=reply_keyboard)
        await state.set_state(None)
    elif callback.data == 'lang_zh':
        await state.clear()
        await state.update_data(user=greetings.zh) 
        await callback.message.delete()
        await callback.message.answer(text=greetings.zh,
                                      reply_markup=reply_keyboard)
        await state.set_state(None)
    elif callback.data == 'lang_jp':
        await state.clear()
        await state.update_data(user=greetings.jp)
        await callback.message.delete()
        await callback.message.answer(text=greetings.jp,
                                      reply_markup=reply_keyboard)
        await state.set_state(None)
