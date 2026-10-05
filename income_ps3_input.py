#!/usr/bin/env python3
"""
Mean monthly income per resident aged 10+ (Basico V009, with and without income, R$ of July 2010) by weighting
area, for PS3's initial family income (defect #30). Setor means are weighted by residents in permanent private
households (V002), the closest count to persons aged 10+ in the Basico file.

Not V005 (household head only), and not `average_variance_family_wages.csv`, whose `avg_wage` is this same V009
averaged over setores without weights.
"""

import glob
import os

import numpy as np
import pandas as pd

BASE = '/home/furtado/MyModels/censo2010'
PS3_INPUT = '/home/furtado/MyModels/PS3/input'

aps = pd.read_csv(os.path.join(BASE, 'data/areas_ponderacao_setores.csv'), encoding='utf-16', sep='\t')
aps.columns = ['AREAP', 'Cod_setor']

out = []
for path in sorted(glob.glob(os.path.join(BASE, 'data/setores/*/CSV/Basico_*.csv'))):
    data = pd.read_csv(path, sep=';', encoding='latin-1', dtype=str)
    data = data.rename(columns={data.columns[0]: 'Cod_setor'})
    data['Cod_setor'] = pd.to_numeric(data['Cod_setor'], errors='coerce')
    if data['Cod_setor'].isna().all():
        # Some state CSVs (AC) store the setor code in scientific notation; the XLS keeps all 15 digits
        xls = glob.glob(os.path.join(os.path.dirname(os.path.dirname(path)), 'EXCEL', 'Basico_*.[xX][lL][sS]'))[0]
        data = pd.read_excel(xls, dtype=str)
        data = data.rename(columns={data.columns[0]: 'Cod_setor'})
        data['Cod_setor'] = pd.to_numeric(data['Cod_setor'], errors='coerce')
    for col in ['V002', 'V009']:
        data[col] = pd.to_numeric(data[col].str.replace(',', '.'), errors='coerce')
    data = data.dropna(subset=['Cod_setor', 'V002', 'V009'])
    data = data[data['V002'] > 0].merge(aps, on='Cod_setor', how='inner')
    data['inc_x_w'] = data['V009'] * data['V002']
    grouped = data.groupby('AREAP')[['inc_x_w', 'V002']].sum()
    grouped['income_per_person'] = np.round(grouped['inc_x_w'] / grouped['V002'], 2)
    out.append(grouped[['income_per_person']].reset_index())
    print(os.path.basename(path), len(grouped))

out = pd.concat(out).drop_duplicates('AREAP').sort_values('AREAP')
out.to_csv(os.path.join(PS3_INPUT, 'income_per_person_AP_2010.csv'), index=False)
print(len(out), 'areas written')
