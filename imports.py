from tokens import *
from openai import OpenAI
from asyncio import CancelledError

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from aiogram.methods import SendSticker
from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.fsm.state import State, StatesGroup
from states import Future

import aiomysql
import random
import asyncio
import logging
import json

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.info
router = Router()
bot = Bot(token=api_key)
model = 'gpt-5-mini-2025-08-07' 
client = OpenAI(api_key=open_key)