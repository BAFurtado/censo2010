""" Basic transformation made on original file from IBGE

"""


import pandas as pd

# Making necessary transformation in original file
p = pd.read_csv('sidra_original/tabela202.csv', encoding='utf-8', sep=',', skiprows=5, nrows=5566, header=None)
p = p.drop(columns=[1, 2], axis=1)
p.columns = ['cod_mun', '2000', '2010']
p.replace(to_replace='...', value=0, inplace=True)
p.replace(to_replace='-', value=0, inplace=True)
p[['2000', '2010']] = p[['2000', '2010']].astype(float)
p[['2000', '2010']] = round(p[['2000', '2010']] / 100, 6)
# There was one municipality with values 0, 0 for both years
p = p[p['2010'] != 0]
p.to_csv('input/prop_urban_2000_2010.csv', sep=';', index=False)
