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
email = os.getenv('EMAIL_ADRESS')
email_password = os.getenv('EMAIL_PASSWORD')

languages = {'ru': {'day': 'Мой день', 'week': 'Моя неделя', 'settings': 'Настройки', 'add': 'Добавить', 'back': 'Назад', 'delete': 'Удалить продукт', 'parameters': 'Параметры', 'woman': 'Женщина', 'man': 'Мужчина', 'weight': 'Вес', 'height': 'Рост', 'age': 'Возраст', 'sex': 'Пол', 'search': 'Поиск', 'add_weight': 'Добавить вес', 'another_product': 'Выбрать другой продукт', 'kcal': 'Калории', 'week_st': 'Отчёт за неделю', 'st1': 'Необходимое\nколличество ккал', 'st2': 'Употреблёное\nколличество ккал', 'kcal_sg': 'ккал', 'ate': 'Съел', 'left': 'Осталось', 'neces': 'Надо', 'over': 'Переел', 'g': 'гр', 'dayg': 'день', 'carbohydrates': 'Углеводы', 'protein': 'Белки', 'fats': 'Жиры', 'fiber': 'Волокна', 'kcal100': 'Каллорий на 100г.:', 'weight_ad': 'Введите вес:', 'gm': '(граммы или миллилитры):', 'quantity': 'Колличество', 'help': 'Помощь'},
             'en': {'day': 'My day', 'week': 'My week', 'settings': 'Settings', 'add': 'Add', 'back': 'Back', 'delete': 'Delete product', 'parameters': 'Parameters', 'woman': 'Female', 'man': 'Male', 'weight': 'Weight', 'height': 'Growth', 'age': 'Age', 'sex': 'Gender', 'search': 'Search', 'add_weight': 'Add weight', 'another_product': 'Choose another product', 'kcal': 'Calories', 'week_st': 'Report for the week', 'st1': 'Required\nnumber of kcal', 'st2': 'Number of\nkcal consumed', 'kcal_sg': 'kcal', 'ate': 'Ate', 'left': 'Left', 'neces': 'Necessary', 'over': 'Overeat', 'g': 'gr', 'dayg': 'day', 'carbohydrates': 'Carbohydrates', 'protein': 'Protein', 'fats': 'Fats', 'fiber': 'Fiber', 'kcal100': 'Calories per 100g .:', 'weight_ad': 'Enter weight:', 'gm': '(grams or milliliters):', 'quantity': 'Quantity', 'help': 'Help'},
             'ro': {'day': 'Ziua mea', 'week': 'Săptămâna mea', 'settings': 'Setări', 'add': 'Adăuga', 'back': 'Înapoi', 'delete': 'Sterge produs', 'parameters': 'Parametrii', 'woman': 'Femeie', 'man': 'Barbat', 'weight': 'Greutate', 'height': 'Inaltime', 'age': 'Vârstă', 'sex': 'Sex', 'search': 'Căutare', 'add_weight': 'Adăugați greutate', 'another_product': 'Alegeți un alt produs', 'kcal': 'Calorii', 'week_st': 'Raport pentru săptămână', 'st1': 'Necesara\ncantitatea de kcal', 'st2': 'Consumata\ncantitatea de kcal', 'kcal_sg': 'kcal', 'ate': 'Ai mancat', 'left': 'A ramas', 'neces': 'Necesar', 'over': 'Over', 'g': 'gr', 'dayg': 'zi', 'carbohydrates': 'Carbohidrați', 'protein': 'Proteină', 'fats': 'Grăsimi', 'fiber': 'Fibră', 'kcal100': 'Calorii per 100g.:', 'weight_ad': 'Introduceți greutatea:', 'gm': '(grame sau mililitri):', 'quantity': 'Cantitate', 'help': 'Ajutor'},
             'uk': {'day': 'Мій день', 'week': 'Мій тиждень', 'settings': 'Налаштування', 'add': 'Додати', 'back': 'Назад', 'delete': 'Видалити продукт', 'parameters': 'Параметри', 'woman': 'Жіночий', 'man': 'Жінка', 'weight': 'Вага', 'height': 'Зростання', 'age': 'Вік', 'sex': 'Стать', 'search': 'Пошук', 'add_weight': 'Додати вагу', 'another_product': 'Виберіть інший товар', 'kcal': 'Калорії', 'week_st': 'Звіт за тиждень', 'st1': 'вимагається\nкількість ккал', 'st2': 'Число\nспожиті ккал', 'kcal_sg': 'ккал', 'ate': 'Їли', 'left': 'Вліво', 'neces': 'Необхідний', 'over': 'Переїдати', 'g': 'г', 'dayg': 'день', 'carbohydrates': 'Вуглеводи', 'protein': 'Білок', 'fats': 'Жири', 'fiber': 'Волокно', 'kcal100': 'Калорії на 100 г:', 'weight_ad': 'Введіть вагу:', 'gm': '(грами або мілілітри):', 'quantity': 'Кількість', 'help': 'Допомога'},
             'ja': {'day': '私の一日', 'week': '私の一週', 'settings': '設定', 'add': '追加', 'back': '戻る', 'delete': '製品を削除する', 'parameters': 'パラメーター', 'woman': '女性', 'man': '男', 'weight': '重さ', 'height': '成長', 'age': '年', 'sex': '性別', 'search': '探す', 'add_weight': '重量を追加する', 'another_product': '別の製品を選択してください', 'kcal': 'カロリー', 'week_st': '今週のレポート', 'st1': '必須\nkcalの数', 'st2': 'の数\n消費されたkcal', 'kcal_sg': 'kcal', 'ate': '食べた', 'left': '左', 'neces': '必要', 'over': '食べ過ぎ', 'g': 'gr', 'dayg': '日', 'carbohydrates': '炭水化物', 'protein': 'タンパク質', 'fats': '脂肪', 'fiber': 'ファイバ', 'kcal100': '100gあたりのカロリー。：', 'weight_ad': '体重を入力してください：', 'gm': '（グラムまたはミリリットル）：', 'quantity': '量', 'help': 'ヘルプ'},
             'de': {'day': 'Mein Tag', 'week': 'Meine Woche', 'settings': 'Einstellungen', 'add': 'Hinzufügen', 'back': 'Zurück', 'delete': 'Produkt löschen', 'parameters': 'Parameter', 'woman': 'Weiblich', 'man': 'Männlich', 'weight': 'Gewicht', 'height': 'Wachstum', 'age': 'Alter', 'sex': 'Geschlecht', 'search': 'Suche', 'add_weight': 'Gewicht hinzufügen', 'another_product': 'Wählen Sie ein anderes Produkt', 'kcal': 'Kalorien', 'week_st': 'Bericht für die Woche', 'st1': 'Erforderlich\nAnzahl kcal', 'st2': 'Anzahl von\nkcal verbraucht', 'kcal_sg': 'kcal', 'ate': 'Aß', 'left': 'Links', 'neces': 'Notwendig', 'over': 'Zu viel essen', 'g': 'GR', 'dayg': 'Tag', 'carbohydrates': 'Kohlenhydrate', 'protein': 'Eiweiß', 'fats': 'Fette', 'fiber': 'Faser', 'kcal100': 'Kalorien pro 100g.:', 'weight_ad': 'Gewicht eingeben:', 'gm': '(Gramm oder Milliliter):', 'quantity': 'Menge', 'help': 'Hilfe'},
             'ko': {'day': '내 하루', 'week': '나의 일주일', 'settings': '설정', 'add': '추가하다', 'back': '뒤쪽에', 'delete': '제품 삭제', 'parameters': '매개변수', 'woman': '여자', 'man': '남성', 'weight': '무게', 'height': '성장', 'age': '나이', 'sex': '성별', 'search': '찾다', 'add_weight': '무게 추가', 'another_product': '다른 제품 선택', 'kcal': '칼로리', 'week_st': '이번주 보고', 'st1': '필수의\nkcal의 수', 'st2': '수\n소모된 칼로리', 'kcal_sg': 'kcal', 'ate': '먹었다', 'left': '왼쪽', 'neces': '필요한', 'over': '너무 많이 먹다', 'g': 'gr', 'dayg': '일', 'carbohydrates': '탄수화물', 'protein': '단백질', 'fats': '지방', 'fiber': '섬유', 'kcal100': '100g당 칼로리:', 'weight_ad': '체중 입력:', 'gm': '(그램 또는 밀리리터):', 'quantity': '수량', 'help': '돕다'}
             }
