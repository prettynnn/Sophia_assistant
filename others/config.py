from tokens import open_key
from openai import OpenAI
import logging

data = {}

model = 'gpt-4.1-mini-2025-04-14' 
client = OpenAI(api_key=open_key)
logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.info