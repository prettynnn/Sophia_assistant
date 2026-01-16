from routers.main_routers import main_router
from asyncio.exceptions import CancelledError
from others.config import log
from aiogram import Dispatcher, Bot
from tokens import api_key

import asyncio

bot = Bot(token=api_key)

dp = Dispatcher()
dp.include_router(
    main_router
)

async def main():
    try:
        await dp.start_polling(bot)
    except CancelledError:
        pass
    
if __name__ == "__main__":
    asyncio.run(main())
