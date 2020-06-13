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
                temp.columns = [c.lower() for c in temp.columns]
                temp = temp[['geometry'] + [c for c in temp.columns if c.startswith('cd_apon')]]
                try:
                    temp.columns = ['geometry', 'AREAP']
                    output = pd.concat([output, temp])
                except ValueError:
                    print(temp.columns, each)
                    continue

            os.chdir('../../..')
    return output


if __name__ == '__main__':
    site = r'geoftp.ibge.gov.br'
    folder = r'recortes_para_fins_estatisticos/malha_de_areas_de_ponderacao/censo_demografico_2010'
    f = 'temp_downloads'
    # read_amostra.download_from_ibge(site, folder, f)
    # for fl in os.listdir(f):
    #     print(read_amostra.unzip_files_temp(fl, f))
    fl = 'data/temp_downloads'
    o = add_shapes(fl)
    o.to_file('data/areas/official_incomplete_shp_areas.shp')
