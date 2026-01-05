from imports import *
data = {}

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in data:
        data[user_id] = [{'role': 'system', 'content': 'You are a helpful assistant'}]
        await message.answer('How can I help?')

@dp.message()
async def chat_handler(message: types.Message):
    user_id = message.from_user.id
    try:
        if user_id not in data:
            data[user_id] = [{'role': 'system',
                              'content': 'You are a helpful assistant'}]
            
        user_message = message.text
        thinking = await message.answer('Thinking...')
        data[user_id].append({'role': 'user','content': user_message})
        
        text = client.responses.create(model=model,
                                input=data[user_id][-40:],
                                stream=False)
        thinking = await message.answer('Thinking...')
        response = text.output_text
        await thinking.edit_text(response)
    except Exception as e:
        log(f'Error - {e}')
        
async def save_data():
    with open('data.json', 'w') as file:
        json.dump(data, file)
    await asyncio.sleep(500)

async def main():
    try:
        await dp.start_polling(bot)
        await asyncio.create_task(save_data())
    except KeyboardInterrupt as x:
        log(f'This code is completed! - {x}')
    except CancelledError as y:
        log(f'gg')

if __name__ == "__main__":
    asyncio.run(main())