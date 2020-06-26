""" Gets a metropolitan region choice and returns a dictionary with male and female proportion of population
by age groups.
"""

import pandas as pd


p_etnias = {'cor': ['branca', 'preta', 'amarela', 'parda', 'indigena'],
            'PROP': [47.52, 7.52, 1.1, 43.43, .43]}
etnias2000 = pd.DataFrame.from_dict(p_etnias)
etnias2010 = pd.read_csv('input/2010/etnia_ap.csv', sep=';')

wage_family_data = pd.read_csv('input/2010/average_variance_family_wages.csv', sep=';')
wage_family_data['std_wage'] = wage_family_data['var_wage'] ** 1/2
wage_family_data = wage_family_data[['AREAP', 'avg_num_people', 'avg_wage', 'std_wage']]
