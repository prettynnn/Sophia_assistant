from aiogram import Router

from .callbacks import callback_router
from .fsm import fsm_router
from .text_routers import text_router
from .start_routers import start_router

main_router = Router()

main_router.include_routers(
    start_router,
    callback_router,
    fsm_router,
    text_router
    )
