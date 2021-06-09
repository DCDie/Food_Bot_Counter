import io

import matplotlib.pyplot as plt

from views import counting_necessary_kcal


def week_statistics_graph(user_id, high, latitude, values, plt):
    kcal = counting_necessary_kcal(user_id)
    plt.bar(high, latitude, tick_label=values,
            width=0.3, label='Kcal')
    x_coordinates = [0, 7]
    y_coordinates = [kcal, kcal]
    plt.plot(x_coordinates, y_coordinates, color='red')
    plt.ylabel('Калории')
    plt.title(f'Отчёт за неделю')
    plt.legend([f'Необходимое\nколличество kcal', 'Употреблёное\nколличество kcal'])
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf


def diagram_factory(curent, target, name, units, bar, buf):
    if target - curent > 0:
        colors = ['#00cc66', '#b3ffd9']
        slices = [curent, target - curent]
        activities = [f'Съел - {curent: .0f} {units}', f'Осталось - {(target - curent): .0f} {units}']
        draw_day_statistic_plot(name, colors, activities, slices, bar, buf)
    else:
        colors = ['#00cc00', '#ff3300']
        activities = [f'Надо - {target: .0f} {units}', f'Переел - {(curent - target): .0f} {units}']
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


def diagram_request_sender(carbohydrate, sum_carbohydrates, protein, sum_protein, fat, sum_fat, fiber, sum_fiber):
    plt.figure()
    buf = io.BytesIO()
    plt.subplot(2, 2, 1)
    signification = 'г'
    title = f'Углеводы ({sum_carbohydrates: .0f} {signification}/день )'
    diagram_factory(carbohydrate, sum_carbohydrates, title, signification, plt, buf)
    plt.subplot(2, 2, 2)
    title = f'Белки ({sum_protein: .0f} {signification}/день )'
    diagram_factory(protein, sum_protein, title, signification, plt, buf)
    plt.subplot(2, 2, 3)
    title = f'Жиры ({sum_fat: .0f} {signification}/день )'
    diagram_factory(fat, sum_fat, title, signification, plt, buf)
    plt.subplot(2, 2, 4)
    title = f'Волокна ({sum_fiber: .0f} {signification}/день )'
    buf = diagram_factory(fiber, sum_fiber, title, signification, plt, buf)
    return buf


def draw_big_diagram(kcal, sum_kcal):
    signification = 'kcal'
    title = f'Kcal ({sum_kcal: .0f} {signification} )'
    plt.figure()
    buf = io.BytesIO()
    buf = diagram_factory(kcal, sum_kcal, title, signification, plt, buf)
    plt.close()
    return buf
