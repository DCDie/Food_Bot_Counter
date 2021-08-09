import os
import time
import smtplib
from datetime import datetime, date, timedelta
from email.message import EmailMessage

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from telebot import types
from deep_translator import GoogleTranslator

from buttons import menu, add_food, delete_food
from models import database_dsn, Users, Food, Consumed, FoodLang
from settings import bot, icon, languages, email_password, email

os.environ['TZ'] = 'Europe/Chisinau'
time.tzset()


def users_data(message, language):
    session = sessionmaker(bind=database_dsn)()
    user = session.query(Users.user).filter_by(user=message.from_user.id).first()
    menu_status = 'main'
    if not user:
        MESSAGE = GoogleTranslator(source='auto', target=language).translate(
            f'Привет!\n\nЯ бот. Приятно познакомиться, {message.from_user.first_name}')
        bot.send_message(message.from_user.id, MESSAGE)
        query = Users(user=message.from_user.id, height=170, weight=62, age=30, sex='Мужчина', fname=message.from_user.first_name, lname=message.from_user.last_name)
        session.add(query)
        session.commit()
        MESSAGE = GoogleTranslator(source='auto', target=language).translate(
            f'Пройдите опрос ( Настройки -> Параметры ) чтобы точнее расчитать вашу дневную '
            f'норму питания.\n')
        bot.send_message(message.from_user.id, MESSAGE, reply_markup=menu(menu_status, message, language))
    else:
        MESSAGE = GoogleTranslator(source='auto', target=language).translate(
            f'Привет!\n\nС возвращением, {message.from_user.first_name}!')
        bot.send_message(message.from_user.id, MESSAGE, reply_markup=menu(menu_status, message, language))


def update_weight(message):
    language = message.from_user.language_code
    try:
        weight = float(message.text)
        if weight < 0:
            MESSAGE = GoogleTranslator(source='auto', target=language).translate('Вы ввели отрицательное значение!\n\nВведите ваш вес в кг:')
            sent = bot.send_message(chat_id=message.from_user.id,
                                    text=MESSAGE)
            bot.register_next_step_handler(sent, update_weight)
            return
    except ValueError:
        MESSAGE = GoogleTranslator(source='auto', target=language).translate('Вы ввели не верные данные в {Изменение веса}')
        bot.send_message(chat_id=message.from_user.id, text=MESSAGE,
                         reply_markup=menu('main', message, language))
        return
    session = sessionmaker(bind=database_dsn)()
    session.query(Users).where(Users.user == message.from_user.id).update({Users.weight: weight})
    session.commit()
    MESSAGE = GoogleTranslator(source='auto', target=language).translate('Данные успешно добавлены!\n\nВыберите следующие действие:')
    bot.send_message(chat_id=message.from_user.id, text=MESSAGE,
                     reply_markup=menu('parameters', message, language))


def update_height(message):
    language = message.from_user.language_code
    try:
        height = float(message.text)
        if height < 0:
            MESSAGE = GoogleTranslator(source='auto', target=language).translate('Вы ввели отрицательное значение!\n\nВведите ваш рост в см:')
            sent = bot.send_message(chat_id=message.from_user.id,
                                    text=MESSAGE)
            bot.register_next_step_handler(sent, update_height)
            return
    except ValueError:
        MESSAGE = GoogleTranslator(source='auto', target=language).translate('Вы ввели не верные данные в {Изменение роств}')
        bot.send_message(chat_id=message.from_user.id, text=MESSAGE,
                         reply_markup=menu('main', message, language))
        return
    session = sessionmaker(bind=database_dsn)()
    session.query(Users).where(Users.user == message.from_user.id).update({Users.height: height})
    session.commit()
    MESSAGE = GoogleTranslator(source='auto', target=language).translate('Данные успешно добавлены!\n\nВыберите следующие действие:')
    bot.send_message(chat_id=message.from_user.id, text=MESSAGE,
                     reply_markup=menu('parameters', message, language))


def update_age(message):
    language = message.from_user.language_code
    try:
        age = float(message.text)
        if age < 0:
            MESSAGE = GoogleTranslator(source='auto', target=language).translate('Вы ввели отрицательное значение!\n\nваш возраст в годах:')
            sent = bot.send_message(chat_id=message.from_user.id,
                                    text=MESSAGE)
            bot.register_next_step_handler(sent, update_age)
            return
    except ValueError:
        MESSAGE = GoogleTranslator(source='auto', target=language).translate('Вы ввели не верные данные в {Изменение возраста}')
        bot.send_message(chat_id=message.from_user.id, text=MESSAGE,
                         reply_markup=menu('main', message, language))
        return
    session = sessionmaker(bind=database_dsn)()
    session.query(Users).where(Users.user == message.from_user.id).update({Users.age: age})
    session.commit()
    MESSAGE = GoogleTranslator(source='auto', target=language).translate('Данные успешно добавлены!\n\nВыберите следующие действие:')
    bot.send_message(chat_id=message.from_user.id, text=MESSAGE,
                     reply_markup=menu('parameters', message, language))


def query_add_food_view(food_name, language):
    try:
        lang = languages[language]
    except KeyError:
        lang = languages['en']
    name = food_name.query.lower().split(':')[-1]
    session = sessionmaker(bind=database_dsn)()
    foods = session.query(FoodLang, Food).join(Food).where(
        ((FoodLang.title.contains(name.strip())) & (FoodLang.language == language) & (
                    (Food.added_by == 'admin') | (Food.added_by == f'{food_name.from_user.id}'))) | (
            FoodLang.title.contains(name.strip())) & (
                    (Food.added_by == 'admin') | (Food.added_by == f'{food_name.from_user.id}'))).order_by(
        FoodLang.id).limit(20)
    titles = []
    for i in foods:
        content = types.InputTextMessageContent(
            message_text=f'{i.FoodLang.title.capitalize()} - {i.Food.energy} {lang["kcal_sg"]}/100 {lang["g"]}',
        )

        title = types.InlineQueryResultArticle(
            id=i.FoodLang.id,
            title=i.FoodLang.title.capitalize(),
            description=f'{lang["kcal100"]} {i.Food.energy} {lang["kcal_sg"]}',
            input_message_content=content,
            reply_markup=add_food(i.FoodLang.foodid, food_name.from_user.language_code),
            thumb_url=icon,
            thumb_width=48,
            thumb_height=48
        )
        titles.append(title)

    return food_name.id, titles


def add_new_item(message, food_id):
    msg = message.text
    language = message.from_user.language_code
    try:
        f = float(msg)
    except ValueError:
        MESSAGE = GoogleTranslator(source='auto', target=language).translate('Вы ввели не верные данные!\nВведите вес продукта('
                                                            'граммы или миллилитры)!')
        bot.send_message(chat_id=message.from_user.id, text=MESSAGE,
                         reply_markup=add_food(food_id, language))
        return
    today = datetime.now()
    kind = None
    if today.hour in range(0, 12):
        kind = "BREAKFAST"
    if today.hour in range(12, 17):
        kind = "LUNCH"
    if today.hour in range(17, 24):
        kind = "DINNER"
    session = sessionmaker(bind=database_dsn)()
    food = Consumed(product=food_id, quantity=f, data=today, user=message.from_user.id, food_type=kind)
    session.add(food)
    session.commit()
    MESSAGE = GoogleTranslator(source='auto', target=language).translate('Данные успешно добавлены!\nВыберите следующие действие:')
    bot.send_message(chat_id=message.from_user.id, text=MESSAGE,
                     reply_markup=menu('main', message, language))


def query_delete_food_view(food_name, language):
    foodname = food_name.query.lower().split(':')[-1]
    try:
        lang = languages[language]
    except KeyError:
        lang = languages['en']
    today = date.today()
    session = sessionmaker(bind=database_dsn)()
    calorii = session.query(Consumed, Food).outerjoin(Food, Consumed.product == Food.id).where(
        (Consumed.data == today) &
        (Consumed.user == food_name.from_user.id) &
        (Food.title.contains(foodname.strip())) &
        (Food.id == Consumed.product)).order_by(Consumed.id).limit(20)
    titles = []
    for i in calorii:
        food = session.query(FoodLang).filter((FoodLang.foodid == i.Food.id) & (FoodLang.language == language)).first()
        data = types.InputTextMessageContent(
            message_text=f'{i.Food.title.capitalize()}\n{lang["quantity"]}: {i.Consumed.quantity}'
        )

        record = types.InlineQueryResultArticle(
            id=i.Consumed.id,
            title=food.title.capitalize(),
            description=f'{lang["quantity"]}: {i.Consumed.quantity}',
            input_message_content=data,
            reply_markup=delete_food(i.Consumed.id, food_name.from_user.language_code),
            thumb_url=icon,
            thumb_width=48,
            thumb_height=48
        )
        titles.append(record)
    return food_name.id, titles


def sorting_food_by_type(user, language):
    today = date.today()
    kcal = 0
    carbohydrate = 0
    fiber = 0
    fat = 0
    protein = 0
    session = sessionmaker(bind=database_dsn)()
    query = session.query(Consumed, Food).outerjoin(Food, Consumed.product == Food.id).where(
        (Consumed.user == user) & (Food.id == Consumed.product) &
        (Consumed.data.between(f'{today} 00:00:00', f'{today} 23:59:59')))

    for f in query:
        quantity = f.Consumed.quantity / 100
        kcal += f.Food.energy * quantity
        carbohydrate += f.Food.carbohydrate * quantity
        protein += f.Food.protein * quantity
        fat += f.Food.fat * quantity
        fiber += f.Food.fiber * quantity
    output = list_products_eaten_this_day(user, language)
    return output, kcal, carbohydrate, protein, fat, fiber


def list_products_eaten_this_day(user, language):
    lang = languages[language]
    output = ''
    breakfast = str(f'{lang["breakfast"]}:\n\n')
    lunch = str(f'{lang["lunch"]}:\n\n')
    dinner = str(f'{lang["dinner"]}:\n\n')
    today = date.today()
    session = sessionmaker(bind=database_dsn)()
    query = session.query(Consumed, Food).outerjoin(Food, Consumed.product == Food.id).where(
        (Consumed.user == user) & (Food.id == Consumed.product) &
        (Consumed.data.between(f'{today} 00:00:00', f'{today} 23:59:59')))
    for f in query:
        food = session.query(FoodLang).filter((FoodLang.foodid == f.Food.id) & (FoodLang.language == language)).first()
        if f.Consumed.food_type == 'BREAKFAST':
            breakfast = breakfast + f'{food.title.strip().capitalize()}\n'
        elif f.Consumed.food_type == 'LUNCH':
            lunch = lunch + f'{food.title.strip().capitalize()}\n'
        elif f.Consumed.food_type == 'DINNER':
            dinner = dinner + f'{food.title.strip().capitalize()}\n'
    if breakfast != f'{lang["breakfast"]}:\n\n':
        output = output + f'{breakfast}\n'
    if lunch != f'{lang["lunch"]}:\n\n':
        output = output + f'{lunch}\n'
    if dinner != f'{lang["dinner"]}:\n\n':
        output = output + f'{dinner}\n'
    return output


def counting_necessary_kcal(user_id):
    sum_kcal = float
    session = sessionmaker(bind=database_dsn)()
    user = session.query(Users).where(Users.user == user_id.from_user.id).first()
    if not user:
        query = Users(user=user_id.from_user.id, height=170, weight=62, age=30, sex='Мужчина')
        session.add(query)
        session.commit()
    session = sessionmaker(bind=database_dsn)()
    user = session.query(Users).where(Users.user == user_id.from_user.id)
    for i in user:
        if i.sex == 'Мужчина':
            k = 5
        else:
            k = -161
        sum_kcal = ((10 * i.weight) + (6.25 * i.height) - (5 * i.age) + k) * 1.55
    return sum_kcal


def microelements_counter(sum_kcal):
    kcal_total = sum_kcal / 100
    sum_carbohydrates = kcal_total * 53 / 4.5
    sum_protein = kcal_total * 28 / 4.5
    sum_fat = kcal_total * 14 / 4.66
    sum_fiber = kcal_total * 6 / 4.78
    return sum_carbohydrates, sum_protein, sum_fat, sum_fiber


def iter_week(today=None):
    today = today or date.today()
    monday = today - timedelta(days=today.weekday())
    return today, monday


def collecting_diagram_data(call):
    left = []
    altitude = []
    tick_label = []
    today, monday = iter_week()
    session = sessionmaker(bind=database_dsn)()
    calorii = session.query((func.sum(Consumed.quantity * Food.energy / 100)).label('kcal'), Consumed.data) \
        .outerjoin(Food, Consumed.product == Food.id) \
        .where((Consumed.user == call.from_user.id) & (Food.id == Consumed.product) &
               (Consumed.data.between(monday, f'{today} 23:59:59'))).group_by(Consumed.data)
    for f in calorii:
        left.append(f.data.strftime("%A"))
        altitude.append(float(f.kcal))
        tick_label.append(f'{f.data.strftime("%d")}\n{f.data.strftime("%a")}')
    return left, altitude, tick_label


def help_message(message):
    text = message.text
    msg = EmailMessage()
    msg.set_content(text)
    msg['Subject'] = f'Bot need help! User: {message.from_user.id}'
    msg['From'] = email
    msg['To'] = email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, email_password)
    server.sendmail(email, [email], msg.as_string())
    bot.send_message(message.from_user.id, "Спасибо, мы постараемся помочь!", reply_markup=menu('main', message, message.from_user.language_code))