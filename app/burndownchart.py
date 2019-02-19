# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt, mpld3
import datetime
import numpy as np
import pickle

plt.style.use('seaborn-whitegrid')

variables_path = './variables.dump'

def save_variables(v1, v2, file):
    with open(file, 'wb') as f:
        pickle.dump([v1, v2], f)


def load_variables(file):
    with open(file, 'rb') as f:
        v1, v2 = pickle.load(f)
        return v1, v2


def get_burndown_points(maxy, maxx):
    x = np.arange(maxx)
    y = -(maxy / float(maxx)) * x + maxy
    return x, y


def days_between(d1, d2):
    return abs((d2 - d1).days)


def save_data(path, data):
    np.save(path, data)


def load_progress_data(path):
    y1 = np.load(path)
    return y1


def updated_data(path, init_date_str, curr_date_str, final_date_str, qtd):
    init_date = datetime.datetime.strptime(init_date_str, "%Y-%m-%d")
    curr_date = datetime.datetime.strptime(curr_date_str, "%Y-%m-%d")
    final_date = datetime.datetime.strptime(final_date_str, "%Y-%m-%d")
    past_days = days_between(init_date, curr_date)
    last_past_days, last_maxy = load_variables(variables_path)
    y1 = load_progress_data(path=path)
    remaining_days = days_between(curr_date, final_date)
    maxy = y1[last_past_days] - qtd
    maxx = remaining_days
    x1, new_y1 = get_burndown_points(maxx=maxx, maxy=maxy)
    constant_array = np.repeat(last_maxy, past_days - last_past_days + 1)
    y1= np.concatenate((y1[0:last_past_days-1], constant_array, new_y1), axis=0)
    save_data(path=path, data=y1)
    save_variables(past_days, maxy, variables_path)


def create_chart(path, n_servicos, init_date_str, final_date_str):
    init_date = datetime.datetime.strptime(init_date_str, "%Y-%m-%d")
    final_date = datetime.datetime.strptime(final_date_str, "%Y-%m-%d")
    total_days = days_between(final_date, init_date)
    x1, y1 = get_burndown_points(n_servicos, total_days)
    x1 = np.array([init_date + datetime.timedelta(days=i) for i in range(total_days)])
    x2 = x1.copy()
    y2 = load_progress_data(path)

    fig = plt.figure()
    line_up, = plt.plot(x1, y1, label=u'Referência');
    line_down, = plt.plot(x2, y2, label='Progresso');
    plt.legend(handles=[line_up, line_down])
    plt.xlabel(u'Tempo')
    plt.ylabel(u'Qtd Serviços')
    plt.title(u'Burndown Chart da Digitização de Serviços')
    html_graph = mpld3.fig_to_html(fig)
    return html_graph


def create_initial_data(path, n_servicos, init_date_str, final_date_str):
    init_date = datetime.datetime.strptime(init_date_str, "%Y-%m-%d")
    final_date = datetime.datetime.strptime(final_date_str, "%Y-%m-%d")
    remaining_days = days_between(datetime.datetime.now(), final_date)+1
    curr_date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    curr_date = datetime.datetime.strptime(curr_date_str, "%Y-%m-%d")
    past_days = days_between(curr_date, init_date)
    xn, y2 = get_burndown_points(n_servicos, remaining_days)
    y2_init = np.repeat(n_servicos, past_days)
    y2 = np.concatenate((y2_init, y2), axis=0)
    save_data(path, y2)
    save_variables(past_days, n_servicos, variables_path)



# create_chart(path_progress_data, n_servicos, init_date_str, final_date_str)