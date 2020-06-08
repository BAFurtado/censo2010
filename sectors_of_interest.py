import pandas as pd


muns = pd.read_csv('mun_of_interest.csv', sep=';')
list_muns = list(muns.cod_mun)
list_muns = [str(m) for m in list_muns]