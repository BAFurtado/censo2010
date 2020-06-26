""" Just return a list of mun_codes for a given metropolis
"""

import os
if __name__ == '__main__':
    os.chdir('../..')
import pandas as pd


def list_mun_codes(params):
    data = pd.read_csv('input/ACPs_MUN_CODES.csv', sep=';', header=0, decimal=',')
    return list(data[data.ACPs == params['PROCESSING_ACPS'][0]]['cod_mun'])


if __name__ == '__main__':
    p = dict()
    p['PROCESSING_ACPS'] = ['SALVADOR']
    my_geo = list_mun_codes(p)


