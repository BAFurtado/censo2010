""" Files of Area de Ponderacao by UFs are incomplete.
    Starting again from scratch.
    Reading ALL census tract and dissolving them into APs.
    """

import ftplib
import os
from zipfile import ZipFile

import geopandas as gpd
import pandas as pd


def download_from_ibge(path, directory, flag='shapes_setores'):
    """ Download all zip files of census tract data """
    if not os.path.exists(os.path.join('data', flag)):
        os.makedirs(os.path.join('data', flag))
    ftp = ftplib.FTP(path)
    ftp.login("anonymous", "sectors")
    ftp.cwd(directory)
    files = ftp.nlst()
    for file in files:
        if len(file) == 2:
            ftp.cwd(file)
            archives = ftp.nlst()
            print(archives)
            for each in archives:
                if 'setores' in each:
                    if each.endswith('.zip'):
                        with open(os.path.join('data', flag, each), 'wb') as f:
                            ftp.retrbinary('RETR ' + each, f.write)
            ftp.cwd('..')


def unzipping_census_tract(file, flag):
    with ZipFile(os.path.join(file), 'r') as zip_ref:
        # Extracting all the files
        path = zip_ref.namelist()
        zip_ref.extractall(flag)
    os.remove(file)
    return path


def read_census_tracts_by_uf():
    pass


def add_shapes(flag, aps_setores):
    files = os.listdir(flag)
    shps = [x for x in files if x.endswith('.shp')]
    for file in shps:
        temp = gpd.read_file(os.path.join(flag, file))
        temp = temp.merge(aps_setores, on='CD_GEOCODI')
        temp = temp[['AREAP', 'geometry']]

    return


def main(path, directory, flag, data_flag):
    download_from_ibge(path, directory, flag)
    files = os.listdir(data_fl)
    paths = list()
    for file in files:
        paths.append(unzipping_census_tract(os.path.join(data_flag, file), data_flag))


if __name__ == '__main__':
    site = r'geoftp.ibge.gov.br'
    folder = r'organizacao_do_territorio/malhas_territoriais/malhas_de_setores_censitarios__divisoes_intramunicipais/censo_2010/setores_censitarios_shp/'
    fl = 'shapes_setores'
    data_fl = 'data/shapes_setores'
    aps = pd.read_csv('data/areas_ponderacao_setores.csv', encoding='utf-16', sep='\t')
    aps = aps.rename(columns={'setor': 'CD_GEOCODI'})
    aps.CD_GEOCODI = aps.CD_GEOCODI.astype(str)
    # main(site, folder, fl, data_fl)
    add_shapes(data_fl)


