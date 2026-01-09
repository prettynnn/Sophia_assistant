from aiogram import Router

from routers.start_routers import start_router
from routers.callbacks import callback_router
from routers.fsm import fsm_router
from routers.text_routers import text_router

main_router = Router()

main_router.include_routers(
    start_router,
    callback_router,
    fsm_router,
    text_router,
    )