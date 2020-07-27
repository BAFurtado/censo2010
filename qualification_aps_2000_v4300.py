import pandas as pd
import os
from read_amostra import download_from_ibge
from read_amostra import unzip_files_temp
from read_amostra import extract_txt, convert_to_decimals


names_columns_weighted_areas = ['AREAP', 'weight', 'V4300']
converters = {'AREAP': str, 'weight': convert_to_decimals, 'V4300': str}
# Position is one less than official one (python starts at 0)
columns_weighted_areas = [(50, 63), (334, 345), (167, 169)]


def main(download=False, unzip=False):
    if download:
        download_from_ibge(site, folder, flag)
    directory = os.path.join('data', flag)
    files = os.listdir(directory)
    if unzip:
        for file in files:
            unzip_files_temp(file, directory)
    # Extracting info of V4300


if __name__ == '__main__':
    site = r"ftp.ibge.gov.br"
    folder = r'Censos/Censo_Demografico_2000/Microdados'
    flag = 'amostra_2000'
    main()

