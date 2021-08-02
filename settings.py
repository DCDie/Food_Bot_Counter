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
             'en': {'day': 'My day', 'week': 'My week', 'settings': 'Settings', 'add': 'Add', 'back': 'Back', 'delete': 'Delete product', 'parameters': 'Parameters', 'woman': 'Female', 'man': 'Male', 'weight': 'Weight', 'height': 'Growth', 'age': 'Age', 'sex': 'Gender', 'search': 'Search', 'add_weight': 'Add weight', 'another_product': 'Choose another product', 'kcal': 'Calories', 'week_st': 'Report for the week', 'st1': 'Required\nnumber of kcal', 'st2': 'Number of\nkcal consumed', 'kcal_sg': 'kcal', 'ate': 'Ate', 'left': 'Left', 'neces': 'Necessary', 'over': 'Overeat', 'g': 'gr', 'dayg': 'day', 'carbohydrates': 'Carbohydrates', 'protein': 'Protein', 'fats': 'Fats', 'fiber': 'Fiber', 'kcal100': 'Calories per 100g .:', 'weight_ad': 'Enter weight:', 'gm': '(grams or milliliters):', 'quantity': 'Quantity'},
             'ro': {'day': 'Ziua mea', 'week': 'Săptămâna mea', 'settings': 'Setări', 'add': 'Adăuga', 'back': 'Înapoi', 'delete': 'Sterge produs', 'parameters': 'Parametrii', 'woman': 'Femeie', 'man': 'Barbat', 'weight': 'Greutate', 'height': 'Inaltime', 'age': 'Vârstă', 'sex': 'Sex', 'search': 'Căutare', 'add_weight': 'Adăugați greutate', 'another_product': 'Alegeți un alt produs', 'kcal': 'Calorii', 'week_st': 'Raport pentru săptămână', 'st1': 'Necesara\ncantitatea de kcal', 'st2': 'Consumata\ncantitatea de kcal', 'kcal_sg': 'kcal', 'ate': 'Ai mancat', 'left': 'A ramas', 'neces': 'Necesar', 'over': 'Over', 'g': 'gr', 'dayg': 'zi', 'carbohydrates': 'Carbohidrați', 'protein': 'Proteină', 'fats': 'Grăsimi', 'fiber': 'Fibră', 'kcal100': 'Calorii per 100g.:', 'weight_ad': 'Introduceți greutatea:', 'gm': '(grame sau mililitri):', 'quantity': 'Cantitate'},
             'uk': {'day': 'Мій день', 'week': 'Мій тиждень', 'settings': 'Налаштування', 'add': 'Додати', 'back': 'Назад', 'delete': 'Видалити продукт', 'parameters': 'Параметри', 'woman': 'Жіночий', 'man': 'Жінка', 'weight': 'Вага', 'height': 'Зростання', 'age': 'Вік', 'sex': 'Стать', 'search': 'Пошук', 'add_weight': 'Додати вагу', 'another_product': 'Виберіть інший товар', 'kcal': 'Калорії', 'week_st': 'Звіт за тиждень', 'st1': 'вимагається\nкількість ккал', 'st2': 'Число\nспожиті ккал', 'kcal_sg': 'ккал', 'ate': 'Їли', 'left': 'Вліво', 'neces': 'Необхідний', 'over': 'Переїдати', 'g': 'NS', 'dayg': 'день', 'carbohydrates': 'Вуглеводи', 'protein': 'Білок', 'fats': 'Жири', 'fiber': 'Волокно', 'kcal100': 'Калорії на 100 г:', 'weight_ad': 'Введіть вагу:', 'gm': '(грами або мілілітри):', 'quantity': 'Кількість'}
             }
