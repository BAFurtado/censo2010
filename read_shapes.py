import os
import read_amostra
import geopandas as gpd
import pandas as pd


def add_shapes(flag):
    output = gpd.GeoDataFrame()
    for file in os.listdir(flag):
        if os.path.isdir(os.path.join(flag, file)):
            os.chdir(os.path.join(flag, file))
            shp = [x for x in os.listdir('.') if x.endswith('shp')]
            for each in shp:
                try:
                    temp = gpd.read_file(each)
                except IndexError:
                    continue
                output = pd.concat([output, temp])
            os.chdir('../../..')
    return output


if __name__ == '__main__':
    site = r'geoftp.ibge.gov.br'
    folder = r'recortes_para_fins_estatisticos/malha_de_areas_de_ponderacao/censo_demografico_2010'
    # read_amostra.download_from_ibge(site, folder, 'shapes')
    f = 'data/shapes'
    # for file in os.listdir(flag):
    #     print(read_amostra.unzip_files_temp(file, flag))
    o = add_shapes(f)
