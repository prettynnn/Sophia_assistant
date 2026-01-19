from aiogram import types, Router, Bot
from aiogram.utils.chat_action import ChatActionSender
from aiogram.enums import ChatAction

from tokens import api_key
from others.cfg import model, client, log
from database.roles import user, assistant
from database.memory import connector_to_server, include_in_table, select_data_from_table

text_router = Router()
bot = Bot(token=api_key)

@text_router.message()
async def request_bot_handler(message: types.Message):
    user_id = message.from_user.id
    # chat_id = message.chat.id
    
    connect = await connector_to_server()
    # users = await select_id_from_table(connect, user_id)
    try:
        user_content = message.text
        await include_in_table(connect, user_id, user, user_content)
        await message.bot.send_chat_action(action=ChatAction.TYPING,
                                           chat_id=message.chat.id)
        thinking = await message.answer('Thinking...')
        
        context = []
        data = await select_data_from_table(connect, user_id)
        
        for role, content in data:
            context.insert(0, 
                {'role': role,
                 'content': content}
                )
        text = client.responses.create(model=model,
                                       input=context,
                                       stream=False)
        response = text.output_text
        await message.bot.send_chat_action(action=ChatAction.TYPING,
                                           chat_id=message.chat.id)
        await thinking.edit_text(response)
        
        context.clear()
        await include_in_table(connect, user_id, assistant, response)
    except Exception as e:
        log(f'Error - {e}')
