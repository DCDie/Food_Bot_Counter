from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt
from buttons import menu, search, delete
from graphs import draw_big_diagram, diagram_request_sender, week_statistics_graph
from models import database_dsn, Users, Food, Consumed
from settings import bot, languages
from deep_translator import GoogleTranslator
from views import users_data, update_weight, update_height, update_age, query_add_food_view, add_new_item, \
    query_delete_food_view, sorting_food_by_type, counting_necessary_kcal, microelements_counter, \
    collecting_diagram_data


@bot.message_handler(commands=['start'])
def welcome(message):
    language = message.from_user.language_code
    return users_data(message, language)


@bot.message_handler(regexp='⚙')
def settings_menu(message):
    language = message.from_user.language_code
    MESSAGE = GoogleTranslator(source='auto', target=language).translate('Выбери следующие действие:')
    menu_status = 'settings'
    bot.send_message(message.from_user.id, MESSAGE,
                     reply_markup=menu(menu_status, message, language))


@bot.message_handler(regexp='🔙')
def back_button(message):
    language = message.from_user.language_code
    MESSAGE = GoogleTranslator(source='auto', target=language).translate('Выбери следующие действие:')
    menu_status = 'main'
    bot.send_message(message.from_user.id, MESSAGE,
                     reply_markup=menu(menu_status, message, language))


@bot.message_handler(regexp='🔬')
def parameters_menu(message):
    language = message.from_user.language_code
    MESSAGE = GoogleTranslator(source='auto', target=language).translate('Выбери следующие действие:')
    menu_status = 'parameters'
    bot.send_message(message.from_user.id, MESSAGE,
                     reply_markup=menu(menu_status, message, language))


@bot.message_handler(regexp='⚖')
def weight_menu(message):
    language = message.from_user.language_code
    MESSAGE = GoogleTranslator(source='auto', target=language).translate('Введите ваш вес в кг:')
    send = bot.send_message(message.from_user.id, MESSAGE)
    bot.register_next_step_handler(send, update_weight)


@bot.message_handler(regexp='⏫')
def height_menu(message):
    language = message.from_user.language_code
    MESSAGE = GoogleTranslator(source='auto', target=language).translate('Введите ваш рост в см:')
    send = bot.send_message(message.from_user.id, MESSAGE)
    bot.register_next_step_handler(send, update_height)


@bot.message_handler(regexp='⏳')
def age_menu(message):
    language = message.from_user.language_code
    MESSAGE = GoogleTranslator(source='auto', target=language).translate('Введите ваш возраст в годах:')
    send = bot.send_message(message.from_user.id, MESSAGE)
    bot.register_next_step_handler(send, update_age)


@bot.message_handler(regexp='🚻')
def sex_menu(message):
    language = message.from_user.language_code
    MESSAGE = GoogleTranslator(source='auto', target=language).translate('Выберите ваш пол:')
    bot.send_message(message.from_user.id, MESSAGE, reply_markup=menu('sex', message, language))


@bot.message_handler(regexp='👩🏼')
def sex_menu(message):
    language = message.from_user.language_code
    MESSAGE = GoogleTranslator(source='auto', target=language).translate('Поздравляю, данные успешно добавленны!\n\nВыбери следующие действие:')
    session = sessionmaker(bind=database_dsn)()
    session.query(Users).where(Users.user == message.from_user.id).update({Users.sex: 'Женщина'})
    session.commit()
    bot.send_message(message.from_user.id, MESSAGE,
                     reply_markup=menu('parameters', message, language))


@bot.message_handler(regexp='👨🏻')
def sex_menu(message):
    language = message.from_user.language_code
    MESSAGE = GoogleTranslator(source='auto', target=language).translate('Поздравляю, данные успешно добавленны!\n\nВыбери следующие действие:')
    session = sessionmaker(bind=database_dsn)()
    session.query(Users).where(Users.user == message.from_user.id).update({Users.sex: 'Мужчина'})
    session.commit()
    bot.send_message(message.from_user.id, MESSAGE,
                     reply_markup=menu('parameters', message, language))


@bot.message_handler(regexp='🍎')
def add_food_menu(message):
    language = message.from_user.language_code
    MESSAGE = GoogleTranslator(source='auto', target=language).translate('Нажмите поиск:')
    bot.send_message(message.from_user.id, MESSAGE,
                     reply_markup=search(message.from_user.language_code))


@bot.message_handler(regexp='🗑')
def delete_food_menu(message):
    language = message.from_user.language_code
    MESSAGE = GoogleTranslator(source='auto', target=language).translate('Нажмите поиск:')
    bot.send_message(message.from_user.id, MESSAGE,
                     reply_markup=delete(message.from_user.language_code))


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def view_data(query):
    language = query.from_user.language_code
    if query.query.lower().split(':')[0] == 'add':
        food_name, titles = query_add_food_view(query, language)
        bot.answer_inline_query(food_name, titles, cache_time=False)
    elif query.query.lower().split(':')[0] == 'delete':
        food_name, titles = query_delete_food_view(query, language)
        bot.answer_inline_query(food_name, titles, cache_time=False)


@bot.callback_query_handler(func=lambda call: call.data.startswith('add-food-entry'))
def item_view(message):
    language = message.from_user.language_code
    try:
        lang = languages[language]
    except KeyError:
        lang = languages['en']
    food_id = message.data.split('-')[-1]
    session = sessionmaker(bind=database_dsn)()
    food = session.query(Food).where(Food.id == food_id)
    for i in food:
        MESSAGE = f'{lang["weight_ad"]}\n{GoogleTranslator(source="auto", target=language).translate(i.title)}\n{lang["gm"]}'
        sent = bot.send_message(chat_id=message.from_user.id,
                                text=MESSAGE, reply_markup=menu('masa', message, language))
        bot.register_next_step_handler(sent, add_new_item, food_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete-food-entry'))
def delete_item(message):
    language = message.from_user.language_code
    MESSAGE = GoogleTranslator(source='auto', target=language).translate(f'Запись успешно удаленна!')
    food_id = message.data.split('-')[-1]
    session = sessionmaker(bind=database_dsn)()
    session.query(Consumed).filter_by(id=food_id).delete()
    session.commit()
    bot.send_message(chat_id=message.from_user.id,
                     text=MESSAGE, reply_markup=menu('main', message, language))


@bot.message_handler(regexp='🧾')
def all_day_view(message):
    language = message.from_user.language_code
    user = message.from_user.id
    output, kcal, carbohydrate, protein, fat, fiber = sorting_food_by_type(user, language)
    if not output:
        MESSAGE = GoogleTranslator(source='auto', target=language).translate('Ты ничего сегодня не ел!\nИсправь это!')
        bot.send_message(message.from_user.id, MESSAGE, reply_markup=menu('main', message, language))
        return
    bot.send_message(message.from_user.id, output)
    sum_kcal = counting_necessary_kcal(message)
    img = draw_big_diagram(kcal, sum_kcal, language)
    bot.send_photo(chat_id=message.from_user.id, photo=img)
    sum_carbohydrates, sum_protein, sum_fat, sum_fiber = microelements_counter(sum_kcal)
    img = diagram_request_sender(carbohydrate, sum_carbohydrates, protein, sum_protein, fat, sum_fat, fiber, sum_fiber, language)
    bot.send_photo(chat_id=message.from_user.id, photo=img)
    MESSAGE = GoogleTranslator(source='auto', target=language).translate('Выбери следующие действие:')
    bot.send_message(message.from_user.id, MESSAGE, reply_markup=menu('main', message, language))


@bot.message_handler(regexp='📊')
def week_view(message):
    language = message.from_user.language_code
    try:
        MESSAGE = GoogleTranslator(source='auto', target=language).translate('Выбери следующие действие:')
        left, altitude, tick_label = collecting_diagram_data(message)
        plt.figure()
        buf = week_statistics_graph(message, left, altitude, tick_label, plt, language)
        bot.send_photo(chat_id=message.from_user.id, photo=buf)
        bot.send_message(chat_id=message.from_user.id, text=MESSAGE,
                         reply_markup=menu('main', message, language))
        plt.close()
    except TypeError:
        MESSAGE = GoogleTranslator(source='auto', target=language).translate(f'Ты на этой неделе ничего не ел!')
        bot.send_message(chat_id=message.from_user.id, text=MESSAGE,
                         reply_markup=menu('main', message, language))


bot.polling(none_stop=True, interval=0)
