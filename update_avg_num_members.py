#!/usr/bin/env python3
"""
Populate PS3/input/average_num_members_families_2010.csv with avg_num_people
per AREAP for all new municipalities in mun_of_interest.csv.

Source: Basico_{UF}.csv sector files (V003 = avg household size)
Output: appended rows in PS3/input/average_num_members_families_2010.csv
"""

import os
import sys
import numpy as np
import pandas as pd

BASE = '/home/furtado/MyModels/censo2010'
os.chdir(BASE)
sys.path.insert(0, BASE)

from sectors_of_interest import aps  # full sector→AREAP mapping (unfiltered)

PS3_INPUT = '/home/furtado/MyModels/PS3/input'
SECTOR_BASE = 'data/setores'

muns = pd.read_csv('mun_of_interest.csv', sep=';')
selected_mun_codes = set(muns['cod_mun'].astype(str).unique())

# Load existing file to know what's already covered
avg_path = f'{PS3_INPUT}/average_num_members_families_2010.csv'
existing = pd.read_csv(avg_path)
existing_areaps = set(existing['AREAP'].astype(str).unique())
print(f'Existing AREAPs: {len(existing_areaps)}')

# State directories → Basico file name
state_dirs = {
    'AC': ('Base informaçoes setores2010 universo AC', 'Basico_AC.csv'),
    'AL': ('Base informaçoes setores2010 universo AL', 'Basico_AL.csv'),
    'AM': ('Base informaçoes setores2010 universo AM', 'Basico_AM.csv'),
    'AP': ('Base informaçoes setores2010 universo AP', 'Basico_AP.csv'),
    'BA': ('Base informaçoes setores2010 universo BA', 'Basico_BA.csv'),
    'CE': ('Base informaçoes setores2010 universo CE', 'Basico_CE.csv'),
    'DF': ('Base informaçoes setores2010 universo DF', 'Basico_DF.csv'),
    'ES': ('Base informaçoes setores2010 universo ES', 'Basico_ES.csv'),
    'GO': ('Base informaçoes setores2010 universo GO', 'Basico_GO.csv'),
    'MA': ('Base informaçoes setores2010 universo MA', 'Basico_MA.csv'),
    'MG': ('Base informaçoes setores2010 universo MG', 'Basico_MG.csv'),
    'MS': ('Base informaçoes setores2010 universo MS', 'Basico_MS.csv'),
    'MT': ('Base informaçoes setores2010 universo MT', 'Basico_MT.csv'),
    'PA': ('Base informaçoes setores2010 universo PA', 'Basico_PA.csv'),
    'PB': ('Base informaçoes setores2010 universo PB', 'Basico_PB.csv'),
    'PE': ('Base informaçoes setores2010 universo PE', 'Basico_PE.csv'),
    'PI': ('Base informaçoes setores2010 universo PI', 'Basico_PI.csv'),
    'PR': ('Base informaçoes setores2010 universo PR', 'Basico_PR.csv'),
    'RJ': ('Base informaçoes setores2010 universo RJ', 'Basico_RJ.csv'),
    'RN': ('Base informaçoes setores2010 universo RN', 'Basico_RN.csv'),
    'RO': ('Base informaçoes setores2010 universo RO', 'Basico_RO.csv'),
    'RR': ('Base informaçoes setores2010 universo RR', 'Basico_RR.csv'),
    'RS': ('Base informaçoes setores2010 universo RS', 'Basico_RS.csv'),
    'SC': ('Base informaçoes setores2010 universo SC', 'Basico_SC.csv'),
    'SE': ('Base informaçoes setores2010 universo SE', 'Basico_SE.csv'),
    'SP1': ('Base informaçoes setores2010 universo SP_Capital',   'Basico_SP1.csv'),
    'SP2': ('Base informaçoes setores2010 universo SP_Exceto_Capital', 'Basico_SP2.csv'),
    'TO': ('Base informaçoes setores2010 universo TO', 'Basico_TO.csv'),
}

new_rows = []

for uf, (state_dir, basico_file) in sorted(state_dirs.items()):
    path = os.path.join(SECTOR_BASE, state_dir, 'CSV', basico_file)
    if not os.path.exists(path):
        print(f'  {uf}: {basico_file} not found, skipping')
        continue

    try:
        data = pd.read_csv(path, sep=';', encoding='latin-1', decimal=',')
    except Exception as e:
        print(f'  {uf}: read error — {e}')
        continue

    # Normalise the sector code column name (IBGE sometimes uses BOM prefix)
    if 'Cod_setor' not in data.columns:
        for col in data.columns:
            if 'Cod_setor' in col or 'Cod_se' in col:
                data = data.rename(columns={col: 'Cod_setor'})
                break
        else:
            data['Cod_setor'] = data.iloc[:, 0]

    try:
        data = data[['Cod_setor', 'V003']]   # V003 = avg household size
    except KeyError:
        print(f'  {uf}: V003 column not found, skipping')
        continue

    data = data.rename(columns={'V003': 'avg_num_people'})
    # Sector codes may be read as float (scientific notation) — cast via int
    if data['Cod_setor'].dtype == float:
        data['Cod_setor'] = data['Cod_setor'].apply(
            lambda x: str(int(x)) if pd.notna(x) else None)
        data = data.dropna(subset=['Cod_setor'])
    else:
        data['Cod_setor'] = data['Cod_setor'].astype(str)

    # Merge sector → AREAP (align dtypes first)
    aps_str = aps.copy()
    aps_str['Cod_setor'] = aps_str['Cod_setor'].astype(str)
    merged = pd.merge(data, aps_str, on='Cod_setor', how='inner')
    merged['mun'] = merged['AREAP'].astype(str).str[:7]

    # Filter to new selected municipalities only
    merged = merged[merged['mun'].isin(selected_mun_codes)]
    if len(merged) == 0:
        print(f'  {uf}: no matching municipalities')
        continue

    # Aggregate to AREAP level (mean of sector averages)
    agg = merged.groupby('AREAP')['avg_num_people'].mean().reset_index()
    agg['AREAP'] = agg['AREAP'].astype(str)

    # Keep only AREAPs not already in the file
    new = agg[~agg['AREAP'].isin(existing_areaps)]
    print(f'  {uf}: {len(new)} new APs')
    new_rows.append(new)

if new_rows:
    combined = pd.concat([existing, pd.concat(new_rows, ignore_index=True)], ignore_index=True)
    combined.to_csv(avg_path, index=False)
    print(f'\nSaved. Total AREAPs: {len(combined)}  (added {len(combined) - len(existing)})')
else:
    print('\nNo new rows to add.')