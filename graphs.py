import io

import matplotlib.pyplot as plt
from deep_translator import GoogleTranslator

from settings import languages
from views import counting_necessary_kcal


def week_statistics_graph(user_id, high, latitude, values, plt, language):
    try:
        lang = languages[language]
    except KeyError:
        lang = languages['en']
    kcal = counting_necessary_kcal(user_id)
    values = rename_days(values, language)
    plt.bar(high, latitude, tick_label=values,
            width=0.3, label='kcal')
    x_coordinates = [0, 7]
    y_coordinates = [kcal, kcal]
    plt.plot(x_coordinates, y_coordinates, color='red')
    plt.ylabel(lang['kcal'])
    plt.title(lang['week_st'])
    plt.legend([lang['st1'], lang['st2']])
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf


def rename_days(values, language):
    for i, j in enumerate(values):
        if language != 'en':
            values[i] = GoogleTranslator(source='en', target=language).translate(j)
    return values


def diagram_factory(curent, target, name, units, bar, buf, language):
    try:
        lang = languages[language]
    except KeyError:
        lang = languages['en']
    if target - curent > 0:
        colors = ['#00cc66', '#b3ffd9']
        slices = [curent, target - curent]
        activities = [f'{lang["ate"]} - {curent: .0f} {units}', f'{lang["left"]} - {(target - curent): .0f} {units}']
        draw_day_statistic_plot(name, colors, activities, slices, bar, buf)
    else:
        colors = ['#00cc00', '#ff3300']
        activities = [f'{lang["neces"]} - {target: .0f} {units}', f'{lang["over"]} - {(curent - target): .0f} {units}']
        slices = [target, curent - target]
        draw_day_statistic_plot(name, colors, activities, slices, bar, buf)
    return buf


def draw_day_statistic_plot(name, colors, legend, slices, bar, buf):
    bar.title(name)
    bar.pie(slices, startangle=90, radius=1, colors=colors, explode=(0, 0.1), pctdistance=0.3, shadow=True,
            wedgeprops={'edgecolor': 'black', 'linewidth': 1, 'linestyle': 'solid', 'antialiased': True})
    bar.legend(legend)
    bar.savefig(buf, format='png')
    buf.seek(0)
    return buf


def diagram_request_sender(carbohydrate, sum_carbohydrates, protein, sum_protein, fat, sum_fat, fiber, sum_fiber, language):
    try:
        lang = languages[language]
    except KeyError:
        lang = languages['en']
    plt.figure()
    buf = io.BytesIO()
    plt.subplot(2, 2, 1)
    signification = lang['g']
    title = f'{lang["carbohydrates"]} ({sum_carbohydrates: .0f} {signification}/{lang["dayg"]} )'
    diagram_factory(carbohydrate, sum_carbohydrates, title, signification, plt, buf, language)
    plt.subplot(2, 2, 2)
    title = f'{lang["protein"]} ({sum_protein: .0f} {signification}/{lang["dayg"]} )'
    diagram_factory(protein, sum_protein, title, signification, plt, buf, language)
    plt.subplot(2, 2, 3)
    title = f'{lang["fats"]} ({sum_fat: .0f} {signification}/{lang["dayg"]} )'
    diagram_factory(fat, sum_fat, title, signification, plt, buf, language)
    plt.subplot(2, 2, 4)
    title = f'{lang["fiber"]} ({sum_fiber: .0f} {signification}/{lang["dayg"]} )'
    buf = diagram_factory(fiber, sum_fiber, title, signification, plt, buf, language)
    return buf


def draw_big_diagram(kcal, sum_kcal, language):
    try:
        lang = languages[language]
    except KeyError:
        lang = languages['en']
    signification = lang['kcal_sg']
    title = f'{lang["kcal"]} ({sum_kcal: .0f} {signification} )'
    plt.figure()
    buf = io.BytesIO()
    buf = diagram_factory(kcal, sum_kcal, title, signification, plt, buf, language)
    plt.close()
    return buf
