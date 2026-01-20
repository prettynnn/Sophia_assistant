from aiogram import types, Router
from aiogram.enums import ChatAction

from others.cfg import model, client, log
from database.roles import user, assistant
from openai import AuthenticationError, InternalServerError, APITimeoutError
from database.memory import connector_to_server, include_in_table, select_data_from_table

text_router = Router()

@text_router.message()
async def request_bot_handler(message: types.Message):
    user_id = message.from_user.id
    connect = await connector_to_server()
    try:
        user_request = message.text
        await include_in_table(connect,
                               user_id,
                               user,
                               user_request)
        await message.bot.send_chat_action(action=ChatAction.TYPING,
                                           chat_id=message.chat.id)
        thinking = await message.answer('Thinking...')
        data = await select_data_from_table(connect,
                                            user_id)
        raw_context = []
        for role, content in data:
            raw_context.append({'role': role,
                                'content': content})
        context = raw_context[::-1]
        text = client.responses.create(model=model,
                                       input=context,
                                       stream=False)
        response = text.output_text
        
        await message.bot.send_chat_action(action=ChatAction.TYPING,
                                           chat_id=message.chat.id)
        await thinking.edit_text(response)
        await include_in_table(connect,
                               user_id,
                               assistant,
                               response)
        raw_context.clear()
    except AuthenticationError as x:
        log(f'Your API token is incorrect, replace his! - {x}')
    except InternalServerError as y:
        log(f'Server is overloaded, try again... - {y}')
        await message.reply(text='Service is overloaded now, try again later!')
    except APITimeoutError as z:
        log(f'Server not answers, waiting... - {z}')
        await message.reply(text='Server not reply for your request, please try again!')
