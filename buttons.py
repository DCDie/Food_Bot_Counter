from sqlalchemy.orm import sessionmaker
from telebot import types
from deep_translator import GoogleTranslator
from models import database_dsn, Users

languages = {'ru': {'day': 'Мой день', 'week': 'Моя неделя', 'settings': 'Настройки', 'add': 'Добавить', 'back': 'Назад', 'delete': 'Удалить продукт', 'parameters': 'Параметры', 'woman': 'Женский', 'man': 'Мужской', 'weight': 'Вес', 'height': 'Рост', 'age': 'Возраст', 'sex': 'Пол', 'search': 'Поиск', 'add_weight': 'Добавить вес', 'another_product': 'Выбрать другой продукт'}}

def menu(status, message, language):
    lang = languages[language]
    keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(text=f"{lang['day']} 🧾")
    button2 = types.KeyboardButton(text=f"{lang['week']} 📊")
    button3 = types.KeyboardButton(text=f"{lang['settings']} ⚙")
    button4 = types.KeyboardButton(text=f"{lang['add']} 🍎")
    button9 = types.KeyboardButton(text=f"{lang['back']} 🔙")
    button10 = types.KeyboardButton(text=f"{lang['delete']} 🗑")
    button11 = types.KeyboardButton(text=f"{lang['parameters']} 🔬")
    button12 = types.KeyboardButton(text=f"{lang['woman']} 👩🏼")
    button13 = types.KeyboardButton(text=f"{lang['man']} 👨🏻‍")
    button14 = types.KeyboardButton(text="50")
    button15 = types.KeyboardButton(text="100")
    button16 = types.KeyboardButton(text="150")
    button17 = types.KeyboardButton(text="200")
    button18 = types.KeyboardButton(text="250")
    button19 = types.KeyboardButton(text="300")
    button20 = types.KeyboardButton(text="400")
    button21 = types.KeyboardButton(text="500")
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
            button5 = types.KeyboardButton(text=f"{lang['weight']} ⚖️( {i.weight: .1f} kg )")
            button6 = types.KeyboardButton(text=f"{lang['height']} ⏫ ( {i.height: .1f} cm )")
            button7 = types.KeyboardButton(text=f"{lang['age']} ⏳ ( {i.age: .0f} )")
            button8 = types.KeyboardButton(text=f"{lang['sex']} 🚻 ( {i.sex} )")
            keyboards.row(button5, button6)
            keyboards.row(button7, button8)
            keyboards.row(button9)
    elif status == 'sex':
        keyboards.row(button12)
        keyboards.row(button13)
    elif status == 'masa':
        keyboards.row(button14, button15)
        keyboards.row(button16, button17)
        keyboards.row(button18, button19)
        keyboards.row(button20, button21)
    return keyboards


def search(language):
    lang = languages[language]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f"{lang['search']} 🔎", switch_inline_query_current_chat="add:"))
    return keyboard


def delete(language):
    lang = languages[language]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f"{lang['search']} 🔎", switch_inline_query_current_chat="delete:"))
    return keyboard


def add_food(food_id, language):
    lang = languages[language]
    food = types.InlineKeyboardMarkup()
    food.add(types.InlineKeyboardButton(text=f"{lang['add_weight']} ⚖", callback_data=f"add-food-entry-{food_id}"))
    food.add(types.InlineKeyboardButton(text=f"{lang['another_product']} 🍎", switch_inline_query_current_chat="add:"))
    return food


def delete_food(food_id, language):
    lang = languages[language]
    food = types.InlineKeyboardMarkup()
    food.add(types.InlineKeyboardButton(text=f"{lang['delete']} 🗑", callback_data=f"delete-food-entry-{food_id}"))
    food.add(types.InlineKeyboardButton(text=f"{lang['another_product']} 🗑", switch_inline_query_current_chat="delete:"))
    return food
