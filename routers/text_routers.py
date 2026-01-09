from aiogram import types, Router
from aiogram.utils.chat_action import ChatActionSender

from others.config import data, model, client, log

text_router = Router()

@text_router.message()
async def request_bot_handler(message: types.Message):
    user = message.from_user.id
    chat = message.chat.id
    try:
        if user not in data:
            data[user] = [{'role': 'system',
                           'content': 'You are a helpful assistant a Sophia'}]
        user_message = message.text
        await message.bot.send_chat_action(action='typing',
                                     chat_id=chat)
        thinking = await message.answer('Thinking...')
        data[user].append({'role': 'user',
                           'content': user_message})
        text = client.responses.create(model=model,
                                       input=data[user][-35:],
                                       stream=False)
        response = text.output_text
        await message.bot.send_chat_action(action='typing',
                                           chat_id=chat)
        await thinking.edit_text(response)
        data[user] = [{'role': 'assistant',
                       'content': response}]
    except Exception as e:
        log(f'Error - {e}')