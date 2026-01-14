from routers.main_routers import main_router
from others.config import log, data
from tokens import api_key

from asyncio.exceptions import CancelledError
from aiogram import Dispatcher, Bot

import asyncio
import json

bot = Bot(token=api_key)

dp = Dispatcher()
dp.include_router(
    main_router
)

async def save_data():
    with open('data.json', 'w') as file:
        json.dump(data, file)
    await asyncio.sleep(600)

async def main():
    history = asyncio.create_task(save_data())
    try:
        await dp.start_polling(bot)
    except CancelledError:
        log(f'gg')
    except KeyboardInterrupt:
        log(f'This code is completed!')
        history.cancel()
        await history

if __name__ == "__main__":
    asyncio.run(main())
