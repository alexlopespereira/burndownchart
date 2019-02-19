from burndownchart import create_initial_data

init_date_str = '2019-01-01'
final_date_str = '2020-12-31'
n_servicos = 900

create_initial_data('./progress.npy', n_servicos, init_date_str, final_date_str)