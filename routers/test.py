from imports import *
from keyboards import *
from others import greetings, stickers
from keyboards.inline import inline_keyboard

router = Router()
data = {}

button = [
[types.KeyboardButton(text='🏠 Return to main page')]
]
keyboard = types.ReplyKeyboardMarkup(keyboard=button,
                                    resize_keyboard=True,
                                    one_time_keyboard=False,
                                    input_field_placeholder='Talk to me...')

@router.message(Command('start'))
async def start_handler(message: types.Message, state: FSMContext):
    stick = random.choice(stickers)
    chat = message.chat.id
    user = message.from_user.id
    await bot.send_sticker(sticker=stick,
                                chat_id=chat)
    await bot.send_message(text='Select language',
                           reply_markup=inline_keyboard, 
                           chat_id=chat)
    if user not in data:
        data[user] = [{'role': 'system', 
                        'content': 'You are a helpful assistant is Sophia'}]
        await bot.send_chat_action(action='typing',
                                   chat_id=chat)
    else:
        await bot.send_chat_action(action='typing',
                                   chat_id=chat)
    await state.set_state(Future.language)

@router.callback_query(Future.language)
async def select_lang(callback: CallbackQuery, state: FSMContext):
    user = callback.from_user.id
    chat = callback.message.chat.id
    message = callback.message.message_id
    
    if callback.data == 'lang_en':
       await bot.delete_message(chat_id=chat, message_id=message)
       await bot.send_message(text=greetings.en, chat_id=chat)
       lang_text = greetings.en
       await state.update_data(main_text=lang_text)
    if callback.data == 'lang_ru':
        await bot.delete_message(chat_id=chat, message_id=message)
        await bot.send_message(text=greetings.ru, chat_id=chat)
        lang_text = greetings.ru
        await state.update_data(main_text=lang_text)
    if callback.data == 'lang_zh':
        await bot.delete_message(chat_id=chat, message_id=message)
        await bot.send_message(text=greetings.zh, chat_id=chat)
        lang_text = greetings.zh
        await state.update_data(main_text=lang_text)
    if callback.data == 'lang_jp':
        await bot.delete_message(chat_id=chat, message_id=message)
        await bot.send_message(text=greetings.jp, chat_id=chat)
        lang_text = greetings.jp
        await state.update_data(main_text=lang_text)
    await state.set_state(Future.language)
    
@router.message(F.text == '🏠 Return to main page', Future.language)
async def main_page(message: types.Message, state: FSMContext):
    chat = message.chat.id
    await bot.send_chat_action(action='typing', chat_id=chat)

@router.message()
async def chat_handler(message: types.Message):
    user = message.from_user.id
    chat = message.chat.id
    try:
        if user not in data:
            data[user] = [{'role': 'system',
                           'content': 'You are a helpful assistant'}]
            
        user_message = message.text
        await bot.send_chat_action(action='typing', chat_id=chat)
        thinking = await message.answer('Thinking...')
        data[user].append({'role': 'user',
                           'content': user_message})
        text = client.responses.create(model=model,
                                input=data[user][-35:],
                                stream=False)
        response = text.output_text
        await bot.send_chat_action(action='typing', 
                                   chat_id=chat)
        await thinking.edit_text(response)
        data[user] = [{'role': 'assistant',
                       'content': response}]
    except Exception as e:
        log(f'Error - {e}')
    
async def save_data():
    try:
        with open('data.json', 'w') as file:
            json.dump(data, file)
        await asyncio.sleep(600)
    except CancelledError:
        return

async def main():
    try:
        task = asyncio.create_task(save_data())
        await router.start_polling(bot)
    except KeyboardInterrupt:
        task.cancel()
        await task

if __name__ == "__main__":
    asyncio.run(main())