import ftplib
import os
from zipfile import ZipFile
import pandas as pd
from sectors_of_interest import list_muns


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
        zip_ref.extractall('data/')
    return path


def extract_data(male, female):
    male['mun'] = male['Cod_setor'].astype(str).str[:7]
    male = male[male['mun'].isin(list_muns)]
    if len(male) == 0:
        return
    female['mun'] = female['Cod_setor'].astype(str).str[:7]
    female = female[female['mun'].isin(list_muns)]



def main():
    site = r"ftp.ibge.gov.br"
    folder = r'Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios'
    download_from_ibge(site, folder, 'setores')

    # After downloading, unzip one by one, extract data and delete, except original zipfile
    # Get list of files
    setores = r'data/setores'
    files = os.listdir(setores)
    results = dict()
    for file in files:
        unzipped_path = unzip_files_temp(file)
        try:
            results['male'] = pd.read_csv(os.path.join(setores, unzipped_path[22]))
            results['female'] = pd.read_csv(os.path.join(setores, unzipped_path[23]))
        except FileNotFoundError:
            continue
        extract_data(results['male'], results['female'])

      # delete
    # folder2 = r'Censos/Censo_Demografico_2010/Resultados_Gerais_da_Amostra/Microdados'
    # download_from_ibge(site, folder2, 'amostra')


if __name__ == '__main__':
    main()
