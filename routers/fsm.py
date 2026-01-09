from aiogram import F, types, Router
from others.states import User
from aiogram.fsm.context import FSMContext
from keyboards.inline_keyboards import inline_keyboard

fsm_router = Router()

@fsm_router.message(F.text == '🏠 Return to main page', User.language)
async def return_to_main_page(message: types.Message, state: FSMContext):
    chat = message.chat.id
    data = await state.get_data()
    main_text = data.get('user')
    await message.bot.send_chat_action(action='typing',
                                       chat_id=chat)
    await message.answer(text=f"{main_text}")
    
@fsm_router.message(F.text == '🌏 Change language', User.language)
async def change_language(message: types.Message):
    chat = message.chat.id
    await message.bot.send_chat_action(action='typing',
                                       chat_id=chat)
    await message.reply(text='Select language',
                        reply_markup=inline_keyboard)
    
    