from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from others import greetings
from others.states import User
from keyboards.reply_keyboards import reply_keyboard

callback_router = Router()

@callback_router.callback_query()
async def select_language(callback: CallbackQuery, state: FSMContext):
    await state.set_state(User.language)
    
    if callback.data == 'lang_en':
        await callback.message.delete()
        await callback.message.answer(text=greetings.en,
                                      reply_markup=reply_keyboard)
        await state.update_data(user=greetings.en)
    if callback.data == 'lang_ru':
        await callback.message.delete()
        await callback.message.answer(text=greetings.ru,
                                      reply_markup=reply_keyboard)
        await state.update_data(user=greetings.ru)
    if callback.data == 'lang_zh':
        await callback.message.delete()
        await callback.message.answer(text=greetings.zh,
                                      reply_markup=reply_keyboard)
        await state.update_data(user=greetings.zh)
    if callback.data == 'lang_jp':
        await callback.message.delete()
        await callback.message.answer(text=greetings.jp,
                                      reply_markup=reply_keyboard)
        await state.update_data(user=greetings.jp)
    await state.set_state(User.language)