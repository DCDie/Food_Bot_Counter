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

languages = {'ru': {'day': 'Мой день', 'week': 'Моя неделя', 'settings': 'Настройки', 'add': 'Добавить', 'back': 'Назад', 'delete': 'Удалить продукт', 'parameters': 'Параметры', 'woman': 'Женщина', 'man': 'Мужчина', 'weight': 'Вес', 'height': 'Рост', 'age': 'Возраст', 'sex': 'Пол', 'search': 'Поиск', 'add_weight': 'Добавить вес', 'another_product': 'Выбрать другой продукт', 'kcal': 'Калории', 'week_st': 'Отчёт за неделю', 'st1': 'Необходимое\nколличество ккал', 'st2': 'Употреблёное\nколличество ккал', 'kcal_sg': 'ккал', 'ate': 'Съел', 'left': 'Осталось', 'neces': 'Надо', 'over': 'Переел', 'g': 'гр', 'dayg': 'день', 'carbohydrates': 'Углеводы', 'protein': 'Белки', 'fats': 'Жиры', 'fiber': 'Волокна', 'kcal100': 'Каллорий на 100г.:', 'weight_ad': 'Введите вес:', 'gm': '(граммы или миллилитры):', 'quantity': 'Колличество'},
             'en': {'day': 'My day', 'week': 'My week', 'settings': 'Settings', 'add': 'Add', 'back': 'Back', 'delete': 'Delete product', 'parameters': 'Parameters', 'woman': 'Female', 'man': 'Male', 'weight': 'Weight', 'height': 'Growth', 'age': 'Age', 'sex': 'Gender', 'search': 'Search', 'add_weight': 'Add weight', 'another_product': 'Choose another product', 'kcal': 'Calories', 'week_st': 'Report for the week', 'st1': 'Required\nnumber of kcal', 'st2': 'Number of\nkcal consumed', 'kcal_sg': 'kcal', 'ate': 'Ate', 'left': 'Left', 'neces': 'Necessary', 'over': 'Overeat', 'g': 'gr', 'dayg': 'day', 'carbohydrates': 'Carbohydrates', 'protein': 'Protein', 'fats': 'Fats', 'fiber': 'Fiber', 'kcal100': 'Calories per 100g .:', 'weight_ad': 'Enter weight:', 'gm': '(grams or milliliters):', 'quantity': 'Quantity'}
             }
