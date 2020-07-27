import os

import numpy as np
import pandas as pd

from read_amostra import convert_to_decimals
from read_amostra import download_from_ibge
from read_amostra import unzip_files_temp

names_columns_weighted_areas = ['AREAP', 'weight', 'V4300']
converters = {'AREAP': str, 'weight': convert_to_decimals, 'V4300': str}
# Position is one less than official one (python starts at 0)
columns_weighted_areas = [(50, 63), (334, 345), (167, 169)]


def extract_txt(file_location):
    """ Auxiliary function to read fixed_weighted_files from txt from IBGE
    """
    return pd.read_fwf(file_location, colspecs=columns_weighted_areas, names=names_columns_weighted_areas,
                       header=None, converters=converters)


def main(download=False, unzip=False, extracting=True):
    if download:
        download_from_ibge(site, folder, flag)
    directory = os.path.join('data', flag)
    files = os.listdir(directory)
    if unzip:
        for file in files:
            unzip_files_temp(file, directory)
    # Extracting info of V4300
    results = pd.DataFrame()
    if extracting:
        for file in os.listdir(directory):
            if len(file) == 2:
                for files in os.listdir(os.path.join(directory, file)):
                    if files.startswith('P'):
                        data = extract_txt(os.path.join(directory, file, files))
                        # Weighted
                        data = data.groupby(['AREAP', 'V4300']).sum().reset_index()
                        totals = data.groupby('AREAP').sum()['weight'].reset_index()
                        output = pd.DataFrame(columns=['AREAP', 'value', 'V4300'])
                        for i in data.index:
                            output.loc[i, 'value'] = data.loc[i, 'weight'] / \
                                                     totals[totals['AREAP'] == data.loc[19, 'AREAP']]['weight'].item()
                            output.loc[i, 'AREAP'] = data.loc[i, 'AREAP']
                            output.loc[i, 'V4300'] = data.loc[i, 'V4300']
                        results = pd.concat([results, output.pivot(columns='V4300', index='AREAP', values='value')])
                        break
    results.to_csv('input/2000/quali_aps.csv', sep=';', index=False)
    return results


if __name__ == '__main__':
    site = r"ftp.ibge.gov.br"
    folder = r'Censos/Censo_Demografico_2000/Microdados'
    flag = 'amostra_2000'
    r = main()

