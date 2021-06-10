import os
import time
from datetime import datetime, date, timedelta

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from telebot import types

from buttons import menu, add_food, delete_food
from models import database_dsn, Users, Food, Consumed
from settings import bot, icon, dialogstatus

os.environ['TZ'] = 'Europe/Chisinau'
time.tzset()


def users_data(message):
    session = sessionmaker(bind=database_dsn)()
    user = session.query(Users.user).filter_by(user=message.from_user.id).first()
    if not user:
        query = Users(user=message.from_user.id, height=170, weight=62, age=30, sex='Мужчина')
        session.add(query)
        session.commit()
    menu_status = 'main'
    return menu_status


def update_weight(message):
    try:
        weight = float(message.text)
        if weight < 0:
            sent = bot.send_message(chat_id=message.from_user.id,
                                    text='Вы ввели отрицательное значение!\n\nВведите ваш вес в кг:')
            bot.register_next_step_handler(sent, update_weight)
            return
    except ValueError:
        bot.send_message(chat_id=message.from_user.id, text='Вы ввели не верные данные в {Изменение веса}',
                         reply_markup=menu('main', message))
        return
    session = sessionmaker(bind=database_dsn)()
    session.query(Users).where(Users.user == message.from_user.id).update({Users.weight: weight})
    session.commit()
    bot.send_message(chat_id=message.from_user.id, text='Данные успешно добавлены!\n\nВыберите следующие действие:',
                     reply_markup=menu('parameters', message))


def update_height(message):
    try:
        height = float(message.text)
        if height < 0:
            sent = bot.send_message(chat_id=message.from_user.id,
                                    text='Вы ввели отрицательное значение!\n\nВведите ваш рост в см:')
            bot.register_next_step_handler(sent, update_height)
            return
    except ValueError:
        bot.send_message(chat_id=message.from_user.id, text='Вы ввели не верные данные в {Изменение роств}',
                         reply_markup=menu('main', message))
        return
    session = sessionmaker(bind=database_dsn)()
    session.query(Users).where(Users.user == message.from_user.id).update({Users.height: height})
    session.commit()
    bot.send_message(chat_id=message.from_user.id, text='Данные успешно добавлены!\n\nВыберите следующие действие:',
                     reply_markup=menu('parameters', message))


def update_age(message):
    try:
        age = float(message.text)
        if age < 0:
            sent = bot.send_message(chat_id=message.from_user.id,
                                    text='Вы ввели отрицательное значение!\n\nваш возраст в годах:')
            bot.register_next_step_handler(sent, update_age)
            return
    except ValueError:
        bot.send_message(chat_id=message.from_user.id, text='Вы ввели не верные данные в {Изменение возраста}',
                         reply_markup=menu('main', message))
        return
    session = sessionmaker(bind=database_dsn)()
    session.query(Users).where(Users.user == message.from_user.id).update({Users.age: age})
    session.commit()
    bot.send_message(chat_id=message.from_user.id, text='Данные успешно добавлены!\n\nВыберите следующие действие:',
                     reply_markup=menu('parameters', message))


def query_add_food_view(food_name):
    name = food_name.query.lower().split(':')[-1]
    session = sessionmaker(bind=database_dsn)()
    foods = session.query(Food).filter(Food.title.contains(name)).limit(20)
    titles = []
    for i in foods:
        content = types.InputTextMessageContent(
            message_text=f'{i.title.capitalize()} - {i.energy} kcal/100 гр',
        )

        title = types.InlineQueryResultArticle(
            id=i.id,
            title=i.title.capitalize(),
            description=f'Каллорий на 100г.: {i.energy} kcal',
            input_message_content=content,
            reply_markup=add_food(i.id),
            thumb_url=icon,
            thumb_width=48,
            thumb_height=48
        )
        titles.append(title)

    return food_name.id, titles


def item(message, food_id):
    msg = message.text
    try:
        f = float(msg)
    except ValueError:
        bot.send_message(chat_id=message.from_user.id, text='Вы ввели не верные данные!\nВведите вес продукта('
                                                            'граммы или миллилитры)!',
                         reply_markup=add_food(food_id))
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
    dialogstatus[message.from_user.id] = 0
    bot.send_message(chat_id=message.from_user.id, text='Данные успешно добавлены!\nВыберите следующие действие:',
                     reply_markup=menu('main', message))


def query_delete_food_view(food_name):
    foodname = food_name.query.lower().split(':')[-1]
    today = date.today()
    session = sessionmaker(bind=database_dsn)()
    calorii = session.query(Consumed, Food).outerjoin(Food, Consumed.product == Food.id).where(
        (Consumed.data == today) &
        (Consumed.user == food_name.from_user.id) &
        (Food.title.contains(foodname)) &
        (Food.id == Consumed.product))
    titles = []
    for i in calorii:
        data = types.InputTextMessageContent(
            message_text=f'{i.Food.title.capitalize()}\nКолличество: {i.Consumed.quantity}'
        )

        record = types.InlineQueryResultArticle(
            id=i.Consumed.id,
            title=i.Food.title.capitalize(),
            description=f'Колличество: {i.Consumed.quantity}',
            input_message_content=data,
            reply_markup=delete_food(i.Consumed.id),
            thumb_url=icon,
            thumb_width=48,
            thumb_height=48
        )
        titles.append(record)
    return food_name.id, titles


def sorting_food_by_type(user):
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
    output = list_products_eaten_this_day(user)
    return output, kcal, carbohydrate, protein, fat, fiber


def list_products_eaten_this_day(user):
    output = ''
    breakfast = str('ЗАВТРАК:\n\n')
    lunch = str('ОБЕД:\n\n')
    dinner = str('УЖИН:\n\n')
    today = date.today()
    session = sessionmaker(bind=database_dsn)()
    query = session.query(Consumed, Food).outerjoin(Food, Consumed.product == Food.id).where(
        (Consumed.user == user) & (Food.id == Consumed.product) &
        (Consumed.data.between(f'{today} 00:00:00', f'{today} 23:59:59')))
    for f in query:
        if f.Consumed.food_type == 'BREAKFAST':
            breakfast = breakfast + f'{f.Food.title}\n'
        elif f.Consumed.food_type == 'LUNCH':
            lunch = lunch + f'{f.Food.title}\n'
        elif f.Consumed.food_type == 'DINNER':
            dinner = dinner + f'{f.Food.title}\n'
    if breakfast != 'ЗАВТРАК:\n\n':
        output = output + f'{breakfast}\n'
    if lunch != 'ОБЕД:\n\n':
        output = output + f'{lunch}\n'
    if dinner != 'УЖИН:\n\n':
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
        sum_kcal = ((10 * i.weight) + (6.25 * i.height) - (5 * i.age) + k) * 1.4
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
