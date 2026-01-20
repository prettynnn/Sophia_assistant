from aiogram import Bot
from openai import OpenAI
from tokens import open_key, api_key

import logging
logging.basicConfig(level=logging.INFO, 
                    format="%(message)s")

model = 'model' 
client = OpenAI(api_key=open_key)
bot = Bot(token=api_key)
log = logging.info
