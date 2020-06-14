""" Files of Area de Ponderacao by UFs are incomplete.
    Starting again from scratch.
    Reading ALL census tract and dissolving them into APs.
    """

import ftplib
import os
from zipfile import ZipFile

import geopandas as gpd
import pandas as pd

from sectors_of_interest import list_muns, states_link, aps


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


def census_into_weighted_areas(flag, aps_setores):
    brasil = gpd.GeoDataFrame()
    files = os.listdir(flag)
    shps = [x for x in files if x.endswith('.shp')]
    for file in shps:
        print(f'processing {file}')
        temp = gpd.read_file(os.path.join(flag, file))
        temp = temp.merge(aps_setores, on='CD_GEOCODI')
        if len(temp) == 0:
            continue
        temp = temp[['AREAP', 'geometry']]
        temp['geometry'] = temp['geometry'].buffer(0.000001)
        temp = temp.dissolve(by='AREAP')
        name = file[:2]
        temp.to_file(f'data/areas/{name}.shp')
        brasil = pd.concat([temp, brasil])
    brasil.to_file('data/areas/brasil.shp')


def main(path, directory, flag, data_flag, aps_setores):
    download_from_ibge(path, directory, flag)
    files = os.listdir(data_fl)
    paths = list()
    for file in files:
        paths.append(unzipping_census_tract(os.path.join(data_flag, file), data_flag))
    census_into_weighted_areas(data_flag, aps_setores)


if __name__ == '__main__':
    site = r'geoftp.ibge.gov.br'
    folder = r'organizacao_do_territorio/malhas_territoriais/malhas_de_setores_censitarios__divisoes_intramunicipais/censo_2010/setores_censitarios_shp/'
    fl = 'shapes_setores'
    data_fl = 'data/shapes_setores'
    aps = aps.rename(columns={'Cod_setor': 'CD_GEOCODI'})
    aps.CD_GEOCODI = aps.CD_GEOCODI.astype(str)
    # main(site, folder, fl, data_fl, aps)
    census_into_weighted_areas(data_fl, aps)
