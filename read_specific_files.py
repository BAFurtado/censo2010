import os
import pandas as pd
import read_amostra
import numpy as np
from sectors_of_interest import aps


def read_age_gender(keys):
    """ Auxiliary function to read age and gender from sectors tables
    """
    results = dict()
    output = pd.DataFrame()

    results['male'] = pd.read_csv(keys[0], sep=';')
    results['female'] = pd.read_csv(keys[1], sep=';')

    data = read_amostra.extract_age_gender(results['male'], results['female'])
    data = data.melt(id_vars=['AREAP', 'gender'], var_name=['age'])
    data = data.rename(columns={'value': 'num_people'})
    output = pd.concat([output, data])

    output.to_csv('temp_num_people_age_gender_AP.csv', sep=';', index=False)
    return output


def get_color(file):
    output = pd.DataFrame()
    data = pd.read_csv(file, sep=';')
    data = data[['Cod_setor', 'V002', 'V003', 'V004', 'V005', 'V006']]
    data = data.replace('X', 0)
    data = pd.merge(data, aps, on='Cod_setor', how='inner')
    data = data.astype(int)
    data = data.groupby('AREAP').agg(sum)
    data = data.drop('Cod_setor', axis=1)
    data = data.reset_index()
    names = ['branca', 'preta', 'amarela', 'parda', 'indigena']
    new = pd.DataFrame()
    new['AREAP'] = data['AREAP']
    for each in [1, 2, 3, 4, 5]:
        new[names[each - 1]] = data.apply(lambda x: x[each] / x[1:].sum(), axis=1)
    new = new.melt(id_vars=['AREAP'], var_name=['cor'])
    output = pd.concat([output, new])
    output.to_csv('temp_etnia_AP.csv', sep=';', index=False)
    return output


def get_wage_num_family(file):
    output = pd.DataFrame()

    data = pd.read_csv(file, sep=';', encoding='latin-1', decimal=',')
    # Variables of interest (mu, sigma for number of people per family and nominal wage)
    try:
        data = data[['Cod_setor', 'V003', 'V004', 'V009', 'V010']]
    except KeyError:
        data = data[['ï»¿Cod_setor', 'V003', 'V004', 'V009', 'V010']]
        data = data.rename(columns={'ï»¿Cod_setor': 'Cod_setor'})
    except KeyError:
        print('Problems with column name, using column index instead. Yes. Go figure IBGE')
        print(data.columns)
        data['Cod_setor'] = data.iloc[:, 0]
        data = data[['Cod_setor', 'V003', 'V004', 'V009', 'V010']]
    data = pd.merge(data, aps, on='Cod_setor', how='inner')
    # Average of averages and variances of sectors by weighted areas
    data = data.groupby('AREAP').agg(np.mean)
    data = data.drop('Cod_setor', axis=1)
    data = data.reset_index()
    output = pd.concat([output, data])
    output = output.rename(columns={'V003': 'avg_num_people', 'V004': 'var_num_people',
                                    'V009': 'avg_wage', 'V010': 'var_wage'})
    output.to_csv('temp_average_variance_family_wages.csv', sep=';', index=False)
    return output


def get_weighted_areas(file):
    output = pd.DataFrame()
    data = read_amostra.extract_txt(file)

    # Weighted
    data = data.groupby('AREAP').apply(lambda x: np.bincount(x['V6400'], weights=x['weight'])).reset_index()
    for each in [1, 2, 3, 4]:
        data[each] = data[0].apply(lambda x: x[each] / x.sum())
    # Much slower, but allows to get exception only for lines with no value for level '5'
    for i in data[0].index:
        try:
            data.loc[i, 5] = data.loc[i, 0][5] / data.loc[i, 0].sum()
        except IndexError:
            data.loc[i, 5] = 0
    data = data.drop(0, axis=1)
    data = data.melt(id_vars=['AREAP'], var_name=['qual'])
    output = pd.concat([output, data])

    output.to_csv('temp_quali_AP.csv', sep=';', index=False)

    return output


if __name__ == '__main__':
    # Parece que só precisa atualizar num_people_age_gender

    p1 = r'data/setores/RO/Base informaçoes setores2010 universo RO/CSV/Pessoa11_RO.csv'
    p2 = r'data/setores/RO/Base informaçoes setores2010 universo RO/CSV/Pessoa12_RO.csv'
    k = [p1, p2]

    mun_code = [1100122]

    # output1 = read_age_gender(k)
    p3 = r'data/setores/RO/Base informaçoes setores2010 universo RO/CSV/Pessoa03_RO.csv'
    # output2 = get_color(p3)

    p4 = r'data/setores/RO/Base informaçoes setores2010 universo RO/CSV/Basico_RO.csv'
    # output3 = get_wage_num_family(p4)

    p5 = r'data/amostra/RO/Amostra_Pessoas_11.txt'
    output4 = get_weighted_areas(p5)
