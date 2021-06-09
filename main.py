from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt
from buttons import menu, search, delete
from graphs import draw_big_diagram, diagram_request_sender, week_statistics_graph
from models import database_dsn, Users, Food, Consumed
from settings import bot, dialogstatus
from views import users_data, update_weight, update_height, update_age, query_add_food_view, item, \
    query_delete_food_view, sorting_food_by_type, counting_necessary_kcal, microelements_counter, \
    collecting_diagram_data


@bot.message_handler(commands=['start'])
def welcome(message):
    dialogstatus[message.from_user.id] = 0
    bot.send_message(message.chat.id, f'Привет!\n\nЯ бот. Приятно познакомиться, {message.from_user.first_name}')
    status = users_data(message)
    bot.send_message(message.chat.id, f'Пройдите опрос(Настройки->Параметры) чтобы точнее расчитать вашу дневную '
                                      f'норму питания.\n', reply_markup=menu(status, message))


@bot.message_handler(regexp='Настройки')
def settings_menu(message):
    dialogstatus[message.from_user.id] = 0
    menu_status = 'settings'
    bot.send_message(message.from_user.id, 'Выбери следующие действие:',
                     reply_markup=menu(menu_status, message))


@bot.message_handler(regexp='Назад')
def back_button(message):
    dialogstatus[message.from_user.id] = 0
    menu_status = 'main'
    bot.send_message(message.from_user.id, 'Выбери следующие действие:',
                     reply_markup=menu(menu_status, message))


@bot.message_handler(regexp='Параметры')
def parameters_menu(message):
    dialogstatus[message.from_user.id] = 0
    menu_status = 'parameters'
    bot.send_message(message.from_user.id, 'Выбери следующие действие:',
                     reply_markup=menu(menu_status, message))


@bot.message_handler(regexp='Вес')
def weight_menu(message):
    dialogstatus[message.from_user.id] = 0
    send = bot.send_message(message.from_user.id, 'Введите ваш вес в кг:')
    bot.register_next_step_handler(send, update_weight)


@bot.message_handler(regexp='Рост')
def height_menu(message):
    dialogstatus[message.from_user.id] = 0
    send = bot.send_message(message.from_user.id, 'Введите ваш рост в см:')
    bot.register_next_step_handler(send, update_height)


@bot.message_handler(regexp='Возраст')
def age_menu(message):
    dialogstatus[message.from_user.id] = 0
    send = bot.send_message(message.from_user.id, 'Введите ваш возраст в годах:')
    bot.register_next_step_handler(send, update_age)


@bot.message_handler(regexp='Пол')
def sex_menu(message):
    dialogstatus[message.from_user.id] = 0
    bot.send_message(message.from_user.id, 'Выберите ваш пол:', reply_markup=menu('sex', message))


@bot.message_handler(regexp='Женский')
def sex_menu(message):
    session = sessionmaker(bind=database_dsn)()
    session.query(Users).where(Users.user == message.from_user.id).update({Users.sex: 'Женщина'})
    session.commit()
    dialogstatus[message.from_user.id] = 0
    bot.send_message(message.from_user.id, 'Поздравляю, данные успешно добавленны!\n\nВыбери следующие действие:',
                     reply_markup=menu('main', message))


@bot.message_handler(regexp='Мужской')
def sex_menu(message):
    session = sessionmaker(bind=database_dsn)()
    session.query(Users).where(Users.user == message.from_user.id).update({Users.sex: 'Мужчина'})
    session.commit()
    dialogstatus[message.from_user.id] = 0
    bot.send_message(message.from_user.id, 'Поздравляю, данные успешно добавленны!\n\nВыбери следующие действие:',
                     reply_markup=menu('main', message))


@bot.message_handler(regexp='Добавить')
def add_food_menu(message):
    bot.send_message(message.from_user.id, 'Нажмите поиск:',
                     reply_markup=search())


@bot.message_handler(regexp='Удалить')
def delete_food_menu(message):
    bot.send_message(message.from_user.id, 'Нажмите поиск:',
                     reply_markup=delete())


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def view_data(query):
    if dialogstatus.get(query.from_user.id, 0) != 0:
        return
    dialogstatus[query.from_user.id] = 1
    if query.query.lower().split(':')[0] == 'add':
        food_name, titles = query_add_food_view(query)
        bot.answer_inline_query(food_name, titles, cache_time=False)
        dialogstatus[query.from_user.id] = 0
    elif query.query.lower().split(':')[0] == 'delete':
        food_name, titles = query_delete_food_view(query)
        bot.answer_inline_query(food_name, titles, cache_time=False)
        dialogstatus[query.from_user.id] = 0


@bot.callback_query_handler(func=lambda call: call.data.startswith('add-food-entry'))
def item_view(query):
    if dialogstatus.get(query.from_user.id, 0) != 0:
        return
    dialogstatus[query.from_user.id] = 1
    food_id = query.data.split('-')[-1]
    session = sessionmaker(bind=database_dsn)()
    food = session.query(Food).where(Food.id == food_id)
    for i in food:
        sent = bot.send_message(chat_id=query.from_user.id,
                                text=f'Введите вес\n{i.title}\n(граммы или миллилитры):')
        bot.register_next_step_handler(sent, item, food_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete-food-entry'))
def delete_item(query):
    food_id = query.data.split('-')[-1]
    session = sessionmaker(bind=database_dsn)()
    session.query(Consumed).filter_by(id=food_id).delete()
    session.commit()
    bot.send_message(chat_id=query.from_user.id,
                     text=f'Запись успешно удаленна!', reply_markup=menu('main', query))


@bot.message_handler(regexp='Мой день')
def all_day_view(call):
    if dialogstatus.get(call.from_user.id, 0) != 0:
        return
    dialogstatus[call.from_user.id] = 1
    user = call.from_user.id
    output, kcal, carbohydrate, protein, fat, fiber = sorting_food_by_type(user)
    if not output:
        dialogstatus[call.from_user.id] = 0
        bot.send_message(call.from_user.id, 'Ты ничего сегодня не ел!\nИсправь это!', reply_markup=menu('main', call))
        return
    bot.send_message(call.from_user.id, output)
    sum_kcal = counting_necessary_kcal(call)
    img = draw_big_diagram(kcal, sum_kcal)
    bot.send_photo(chat_id=call.from_user.id, photo=img)
    sum_carbohydrates, sum_protein, sum_fat, sum_fiber = microelements_counter(sum_kcal)
    img = diagram_request_sender(carbohydrate, sum_carbohydrates, protein, sum_protein, fat, sum_fat, fiber, sum_fiber)
    bot.send_photo(chat_id=call.from_user.id, photo=img)
    dialogstatus[call.from_user.id] = 0
    bot.send_message(call.from_user.id, 'Выбери следующие действие:', reply_markup=menu('main', call))


@bot.message_handler(regexp='Моя неделя')
def week_view(call):
    if dialogstatus.get(call.from_user.id, 0) != 0:
        return
    dialogstatus[call.from_user.id] = 1
    try:
        left, altitude, tick_label = collecting_diagram_data(call)
        plt.figure()
        buf = week_statistics_graph(call, left, altitude, tick_label, plt)
        bot.send_photo(chat_id=call.from_user.id, photo=buf)
        dialogstatus[call.from_user.id] = 0
        bot.send_message(chat_id=call.from_user.id, text=f'Выберите следующие действие:', reply_markup=menu('main', call))
        plt.close()
    except TypeError:
        dialogstatus[call.from_user.id] = 0
        bot.send_message(chat_id=call.from_user.id, text=f'Ты на этой неделе ничего не ел!', reply_markup=menu('main', call))


bot.polling(none_stop=True, interval=0)
