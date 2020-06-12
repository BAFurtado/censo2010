import os
import read_amostra


if __name__ == '__main__':
    site = r'geoftp.ibge.gov.br'
    folder = r'recortes_para_fins_estatisticos/malha_de_areas_de_ponderacao/censo_demografico_2010'
    # read_amostra.download_from_ibge(site, folder, 'shapes')
    flag = 'data/shapes'
    for file in os.listdir(flag):
        print(read_amostra.unzip_files_temp(file, flag))
