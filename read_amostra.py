import ftplib
import os
import shutil
from zipfile import ZipFile
from zipfile import BadZipFile

import pandas as pd
import numpy as np
from sectors_of_interest import list_muns, states_link, aps


def convert_to_decimals(x):
    return float(x[:3] + '.' + x[3:])


columns_interest = [i for i in range(36, 136)] + [0, 23]
names_columns_weighted_areas = ['AREAP', 'weight', 'V6400']
converters = {'AREAP': str, 'weight': convert_to_decimals, 'V6400': str}
columns_weighted_areas = [(7, 20), (28, 44), (157, 158)]


def download_from_ibge(path, directory, flag='setores'):
    """ Download all zip files of census tract data """
    ftp = ftplib.FTP(path)
    ftp.login("anonymous", "censo2010")
    ftp.cwd(directory)
    files = ftp.nlst()

    for file in files:
        with open(os.path.join('data', flag, file), 'wb') as f:
            ftp.retrbinary('RETR ' + file, f.write)


def unzip_files_temp(file, flag=r'data/setores'):
    if not os.path.exists(flag):
        os.mkdir(flag)
    # importing required modules
    # opening the zip file in READ mode
    try:
        with ZipFile(os.path.join(flag, file), 'r') as zip_ref:
            # Extracting all the files
            zip_ref.printdir()
            path = zip_ref.namelist()
            if path[0][:2] not in states_link:
                return
            zip_ref.extractall(flag)
    except BadZipFile:
        return
    except IsADirectoryError as e:
        print(e)
        file = os.path.join(flag, file)
        file = os.listdir(file)
        with ZipFile(file[0], 'r') as zip_ref:
            # Extracting all the files
            zip_ref.printdir()
            path = zip_ref.namelist()
            if path[0][:2] not in states_link:
                return
            zip_ref.extractall(flag)
    return path


def extract_data(male, female):
    result = list()
    for each in [male, female]:
        each['mun'] = each['Cod_setor'].astype(str).str[:7]
        each = each[each['mun'].isin(list_muns)]
        if len(each) == 0:
            return
        each = each.iloc[:, columns_interest]
        new_columns = [str(int(x[2:]) - 34) if x.startswith('V0') and x != 'V022' else x for x in each.columns]
        new_columns = [str(int(x[1:]) - 34) if x.startswith('V') and x != 'V022' else x for x in new_columns]
        new_columns = ['0' if x == 'V022' else x for x in new_columns]
        each.columns = new_columns
        each = pd.merge(each, aps, on='Cod_setor', how='inner')

        # Some sectors with less than five residences, have omitted information, included as 'X'. Replace them
        each = each.replace('X', 0)
        each = each.astype(int)
        each = each.groupby('AREAP').agg(sum)
        each = each.drop('Cod_setor', axis=1)
        each = each.reset_index()
        result.append(each)
    male = result[0]
    female = result[1]
    male['gender'] = 2
    female['gender'] = 1
    return pd.concat([male, female])


def get_sectors():
    site = r"ftp.ibge.gov.br"
    folder = r'Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios'
    download_from_ibge(site, folder, 'setores')
    # After downloading, unzip one by one, extract data and delete, except original zipfile
    # Get list of files
    sectors = r'data/setores'
    files = os.listdir(sectors)
    results = dict()
    output = pd.DataFrame()
    for file in files:
        unzipped_path = unzip_files_temp(file, sectors)
        if not unzipped_path:
            continue
        try:
            results['male'] = pd.read_csv(os.path.join(sectors, unzipped_path[22]), sep=';')
            results['female'] = pd.read_csv(os.path.join(sectors, unzipped_path[23]), sep=';')
        except FileNotFoundError:
            continue
        data = extract_data(results['male'], results['female'])
        data = data.melt(id_vars=['AREAP', 'gender'], var_name=['age'])
        data = data.rename(columns={'value': 'num_people'})
        output = pd.concat([output, data])
        shutil.rmtree(os.path.join(sectors, unzipped_path[0]))
    output.to_csv('processed/num_people_age_gender_AP.csv', sep=';', index=False)
    shutil.rmtree(sectors)
    return output


def extract_txt(file_location):
    return pd.read_fwf(file_location, colspecs=columns_weighted_areas, names=names_columns_weighted_areas,
                       header=None, converters=converters)


def get_weighted_areas():
    site = r"ftp.ibge.gov.br"
    folder = r'Censos/Censo_Demografico_2010/Resultados_Gerais_da_Amostra/Microdados'
    # download_from_ibge(site, folder, 'amostra')
    areas = r'data/amostra'
    files = os.listdir(areas)
    output = pd.DataFrame()
    for file in files:
        unzipped_path = unzip_files_temp(file, areas)
        if not unzipped_path:
            continue
        data = extract_txt(os.path.join(areas, unzipped_path[4]))
        # Non-weighted
        # data = data.groupby('AREAP')['V6400'].value_counts()
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
        shutil.rmtree(os.path.join(areas, unzipped_path[0]))
    output.to_csv('processed/quali_aps.csv', sep=';', index=False)
    shutil.rmtree(areas)
    return output


def get_etnia():
    site = r"ftp.ibge.gov.br"
    folder = r'Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios'
    download_from_ibge(site, folder, 'setores')
    # After downloading, unzip one by one, extract data and delete, except original zipfile
    # Get list of files
    sectors = r'data/setores'
    files = os.listdir(sectors)
    output = pd.DataFrame()
    for file in files:
        unzipped_path = unzip_files_temp(file, sectors)
        if not unzipped_path:
            continue
        try:
            data = pd.read_csv(os.path.join(sectors, unzipped_path[14]), sep=';')
        except FileNotFoundError:
            continue
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
            new[names[each - 1]] = data.apply(lambda x: x[each] / x[1:5].sum(), axis=1)
        new = new.melt(id_vars=['AREAP'], var_name=['cor'])
        output = pd.concat([output, new])
        shutil.rmtree(os.path.join(sectors, unzipped_path[0]))
    output.to_csv('processed/etnia_ap.csv', sep=';', index=False)
    shutil.rmtree(sectors)
    return output


if __name__ == '__main__':
    # o = get_sectors()
    # p = get_weighted_areas()
    e = get_etnia()
