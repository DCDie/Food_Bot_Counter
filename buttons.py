from sqlalchemy.orm import sessionmaker
from telebot import types

from models import database_dsn, Users


def menu(status, message):
    keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(text="Мой день 🧾")
    button2 = types.KeyboardButton(text="Моя неделя 📊")
    button3 = types.KeyboardButton(text="Настройки ⚙")
    button4 = types.KeyboardButton(text="Добавить 🍎")
    button9 = types.KeyboardButton(text="Назад 🔙")
    button10 = types.KeyboardButton(text="Удалить продукт 🗑")
    button11 = types.KeyboardButton(text="Параметры 🔬")
    button12 = types.KeyboardButton(text="Женский")
    button13 = types.KeyboardButton(text="Мужской")
    if status == 'main':
        keyboards.row(button1, button2)
        keyboards.row(button4)
        keyboards.row(button3)
    elif status == 'settings':
        keyboards.row(button10)
        keyboards.row(button11)
        keyboards.row(button9)
    elif status == 'parameters':
        session = sessionmaker(bind=database_dsn)()
        user = session.query(Users).filter_by(user=message.from_user.id)
        for i in user:
            button5 = types.KeyboardButton(text=f"Вес ⚖️( {i.weight: .1f} кг)")
            button6 = types.KeyboardButton(text=f"Рост ⏫ ( {i.height: .1f} см)")
            button7 = types.KeyboardButton(text=f"Возраст ⏳ ( {i.age: .0f} )")
            button8 = types.KeyboardButton(text=f"Пол 🚻 ( {i.sex} )")
            keyboards.row(button5, button6)
            keyboards.row(button7, button8)
            keyboards.row(button9)
    elif status == 'sex':
        keyboards.row(button12)
        keyboards.row(button13)
    return keyboards


def search():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Поиск 🔎", switch_inline_query_current_chat="add:"))
    return keyboard


def delete():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Поиск 🔎", switch_inline_query_current_chat="delete:"))
    return keyboard


def add_food(food_id):
    food = types.InlineKeyboardMarkup()
    food.add(types.InlineKeyboardButton(text="Добавить вес ⚖", callback_data=f"add-food-entry-{food_id}"))
    food.add(types.InlineKeyboardButton(text="Выбрать другой продукт 🍎", switch_inline_query_current_chat="add:"))
    return food


def delete_food(food_id):
    food = types.InlineKeyboardMarkup()
    food.add(types.InlineKeyboardButton(text="Удалить продукт 🗑", callback_data=f"delete-food-entry-{food_id}"))
    food.add(types.InlineKeyboardButton(text="Выбрать другой продукт 🗑", switch_inline_query_current_chat="delete:"))
    return food
