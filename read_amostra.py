import ftplib
import os

import pandas as pd


def download_from_ibge(path, directory):
    """ Download all zip files of census tract data """
    ftp = ftplib.FTP(path)
    ftp.login("anonymous", "censo2010")
    ftp.cwd(directory)
    files = ftp.nlst()

    for file in files:
        with open(os.path.join('data', file), 'wb') as f:
            ftp.retrbinary('RETR ' + file, f.write)


def unzip_files_temp(file):
    pass


def extract_data(file):
    pass


if __name__ == '__main__':
    site = r"ftp.ibge.gov.br"
    folder = r'Censos/Censo_Demografico_2010/Resultados_Gerais_da_Amostra/Microdados'
    download_from_ibge(site, folder)
