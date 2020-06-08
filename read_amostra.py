import ftplib
import os
from zipfile import ZipFile
import pandas as pd
from sectors_of_interest import list_muns, states_link, aps


columns_interest = [i for i in range(36, 136)] + [0, 23]


def download_from_ibge(path, directory, flag='setores'):
    """ Download all zip files of census tract data """
    ftp = ftplib.FTP(path)
    ftp.login("anonymous", "censo2010")
    ftp.cwd(directory)
    files = ftp.nlst()

    for file in files:
        with open(os.path.join('data', flag, file), 'wb') as f:
            ftp.retrbinary('RETR ' + file, f.write)


def unzip_files_temp(file):
    # importing required modules
    # opening the zip file in READ mode
    with ZipFile(file, 'r') as zip_ref:
        # extracting all the files
        zip_ref.printdir()
        path = zip_ref.namelist()
        if path[0][:2] not in states_link:
            return
        zip_ref.extractall('data/')
    return path


def extract_data(male, female):
    male['mun'] = male['Cod_setor'].astype(str).str[:7]
    male = male[male['mun'].isin(list_muns)]
    if len(male) == 0:
        return
    female['mun'] = female['Cod_setor'].astype(str).str[:7]
    female = female[female['mun'].isin(list_muns)]
    male = male.iloc[:, columns_interest]
    new_columns = [str(int(x[2:]) - 34) if x.startswith('V0') and x != 'V022' else x for x in male.columns]
    new_columns = [str(int(x[1:]) - 34) if x.startswith('V') and x != 'V022' else x for x in new_columns]
    new_columns = ['0' if x == 'V022' else x for x in new_columns]
    male.columns = new_columns
    female.columns = new_columns
    male['gender'] = 2
    female['gender'] = 1


def main():
    site = r"ftp.ibge.gov.br"
    folder = r'Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios'
    download_from_ibge(site, folder, 'setores')
    # After downloading, unzip one by one, extract data and delete, except original zipfile
    # Get list of files
    sectors = r'data/setores'
    files = os.listdir(sectors)
    results = dict()
    for file in files:
        unzipped_path = unzip_files_temp(file)
        if not unzipped_path:
            continue
        try:
            results['male'] = pd.read_csv(os.path.join(sectors, unzipped_path[22]))
            results['female'] = pd.read_csv(os.path.join(sectors, unzipped_path[23]))
        except FileNotFoundError:
            continue
        extract_data(results['male'], results['female'])

      # delete
    # folder2 = r'Censos/Censo_Demografico_2010/Resultados_Gerais_da_Amostra/Microdados'
    # download_from_ibge(site, folder2, 'amostra')


if __name__ == '__main__':
    main()
