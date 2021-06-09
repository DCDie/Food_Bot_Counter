import os
from typing import Dict

import telebot as telebot
import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

FOOD_IMAGE = os.getenv('FOOD_IMAGE')
icon = FOOD_IMAGE
dialogstatus: Dict[int, int] = {}

database = os.getenv('DATA_BASE')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('DATA_HOST')
port = os.getenv('PORT')