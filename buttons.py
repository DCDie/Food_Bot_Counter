from sqlalchemy.orm import sessionmaker
from telebot import types
from models import database_dsn, Users
from settings import languages

def menu(status, message, language):
    try:
        lang = languages[language]
    except KeyError:
        lang = languages['ru']
    keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(text=f"{lang['day']} ๐งพ")
    button2 = types.KeyboardButton(text=f"{lang['week']} ๐")
    button3 = types.KeyboardButton(text=f"{lang['settings']} โ")
    button4 = types.KeyboardButton(text=f"{lang['add']} ๐")
    button9 = types.KeyboardButton(text=f"{lang['back']} ๐")
    button10 = types.KeyboardButton(text=f"{lang['delete']} ๐")
    button11 = types.KeyboardButton(text=f"{lang['parameters']} ๐ฌ")
    button12 = types.KeyboardButton(text=f"{lang['woman']} ๐ฉ๐ผ")
    button13 = types.KeyboardButton(text=f"{lang['man']} ๐จ๐ปโ")
    button22 = types.KeyboardButton(text=f"{lang['help']} โโ")
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
        keyboards.row(button11, button22)
        keyboards.row(button9)
    elif status == 'parameters':
        session = sessionmaker(bind=database_dsn)()
        user = session.query(Users).filter_by(user=message.from_user.id)
        for i in user:
            button5 = types.KeyboardButton(text=f"{lang['weight']} โ๏ธ( {i.weight: .1f} kg )")
            button6 = types.KeyboardButton(text=f"{lang['height']} โซ ( {i.height: .1f} cm )")
            button7 = types.KeyboardButton(text=f"{lang['age']} โณ ( {i.age: .0f} )")
            if i.sex == 'ะัะถัะธะฝะฐ':
                button8 = types.KeyboardButton(text=f"{lang['sex']} ๐ป ( {lang['man']} )")
            else:
                button8 = types.KeyboardButton(text=f"{lang['sex']} ๐ป ( {lang['woman']} )")
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
    try:
        lang = languages[language]
    except KeyError:
        lang = languages['ru']
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f"{lang['search']} ๐", switch_inline_query_current_chat="add:"))
    return keyboard


def delete(language):
    try:
        lang = languages[language]
    except KeyError:
        lang = languages['ru']
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=f"{lang['search']} ๐", switch_inline_query_current_chat="delete:"))
    return keyboard


def add_food(food_id, language):
    try:
        lang = languages[language]
    except KeyError:
        lang = languages['ru']
    food = types.InlineKeyboardMarkup()
    food.add(types.InlineKeyboardButton(text=f"{lang['add_weight']} โ", callback_data=f"add-food-entry-{food_id}"))
    food.add(types.InlineKeyboardButton(text=f"{lang['another_product']} ๐", switch_inline_query_current_chat="add:"))
    return food


def delete_food(food_id, language):
    try:
        lang = languages[language]
    except KeyError:
        lang = languages['ru']
    food = types.InlineKeyboardMarkup()
    food.add(types.InlineKeyboardButton(text=f"{lang['delete']} ๐", callback_data=f"delete-food-entry-{food_id}"))
    food.add(types.InlineKeyboardButton(text=f"{lang['another_product']} ๐", switch_inline_query_current_chat="delete:"))
    return food
