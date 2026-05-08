#!/usr/bin/env python3
"""
Add census 2010 data for ACUs missing from PS3/input.
Processes num_people (sector files) and qualification (amostra files) for:
RR, RO, AC, TO, SC, RS
"""

import os
import sys
from zipfile import ZipFile

import numpy as np
import pandas as pd

BASE = '/home/furtado/MyModels/censo2010'
os.chdir(BASE)
sys.path.insert(0, BASE)

import read_amostra
from sectors_of_interest import list_muns

PS3_INPUT = '/home/furtado/MyModels/PS3/input'
SECTOR_BASE = 'data/setores'
AMOSTRA_BASE = 'data/amostra'


def compute_num_people(sector_dir, male_f, female_f):
    male = pd.read_csv(os.path.join(sector_dir, male_f), sep=';')
    female = pd.read_csv(os.path.join(sector_dir, female_f), sep=';')
    data = read_amostra.extract_age_gender(male, female)
    if data is None or len(data) == 0:
        return None
    data = data.melt(id_vars=['AREAP', 'gender'], var_name='age')
    data = data.rename(columns={'value': 'num_people'})
    data['mun'] = data['AREAP'].astype(str).str[:7].astype(int)
    return data


def compute_quali(amostra_txt):
    data = read_amostra.extract_txt(amostra_txt)
    data['V6400'] = pd.to_numeric(data['V6400'], errors='coerce')
    data = data.dropna(subset=['V6400'])
    data['V6400'] = data['V6400'].astype(int)
    data = data[data['V6400'] > 0]

    grouped = data.groupby('AREAP').apply(
        lambda x: np.bincount(x['V6400'].values, weights=x['weight'].values, minlength=6)
    ).reset_index()

    rows = []
    for _, row in grouped.iterrows():
        counts = row[0]
        total = counts.sum()
        if total == 0:
            continue
        for qual in [1, 2, 3, 4, 5]:
            try:
                val = counts[qual] / total
            except IndexError:
                val = 0.0
            rows.append({'AREAP': row['AREAP'], 'qual': qual, 'value': val})

    return pd.DataFrame(rows)


def quali_to_ps3(df):
    """Convert long (AREAP, qual, value) to PS3 cumulative wide (code, 1-5).
    Columns are kept as strings to match what pd.read_csv returns for the existing file."""
    wide = df.pivot(index='AREAP', columns='qual', values='value').fillna(0)
    wide = wide.reindex(columns=[1, 2, 3, 4, 5], fill_value=0)
    wide = wide.cumsum(axis=1)
    wide[5] = 1.0
    wide.index.name = 'code'
    wide = wide.reset_index()
    # Rename integer columns to strings so they align with the CSV-read column names
    wide.columns = [str(c) if c != 'code' else c for c in wide.columns]
    return wide


# ─── Extract RS amostra if needed ────────────────────────────────────────────
rs_txt = f'{AMOSTRA_BASE}/RS/Amostra_Pessoas_43.txt'
if not os.path.exists(rs_txt):
    print('Extracting RS.zip...')
    with ZipFile(f'{AMOSTRA_BASE}/RS.zip') as z:
        z.extractall(AMOSTRA_BASE)
    print('Done.')

STATES = [
    ('RR',
     f'{SECTOR_BASE}/Base informaçoes setores2010 universo RR/CSV',
     'Pessoa11_RR.csv', 'Pessoa12_RR.csv',
     f'{AMOSTRA_BASE}/RR/Amostra_Pessoas_14.txt'),
    ('RO',
     f'{SECTOR_BASE}/Base informaçoes setores2010 universo RO/CSV',
     'Pessoa11_RO.csv', 'Pessoa12_RO.csv',
     f'{AMOSTRA_BASE}/RO/Amostra_Pessoas_11.txt'),
    ('AC',
     f'{SECTOR_BASE}/Base informaçoes setores2010 universo AC/CSV',
     'Pessoa11_AC.csv', 'Pessoa12_AC.csv',
     f'{AMOSTRA_BASE}/AC/Amostra_Pessoas_12.txt'),
    ('TO',
     f'{SECTOR_BASE}/Base informaçoes setores2010 universo TO/CSV',
     'Pessoa11_TO.csv', 'Pessoa12_TO.csv',
     f'{AMOSTRA_BASE}/TO/Amostra_Pessoas_17.txt'),
    ('SC',
     f'{SECTOR_BASE}/Base informaçoes setores2010 universo SC/CSV',
     'Pessoa11_SC.csv', 'Pessoa12_SC.csv',
     f'{AMOSTRA_BASE}/SC/Amostra_Pessoas_42.txt'),
    ('RS',
     f'{SECTOR_BASE}/Base informaçoes setores2010 universo RS/CSV',
     'Pessoa11_RS.csv', 'Pessoa12_RS.csv',
     rs_txt),
]

all_num, all_quali = [], []

for state, sector_dir, male_f, female_f, amostra_txt in STATES:
    print(f'\n=== {state} ===')

    print(f'  num_people: {male_f}, {female_f}')
    np_data = compute_num_people(sector_dir, male_f, female_f)
    if np_data is not None and len(np_data):
        print(f'  → {np_data["AREAP"].nunique()} APs, {len(np_data)} rows')
        all_num.append(np_data)
    else:
        print(f'  WARNING: no num_people data')

    print(f'  qualification: {os.path.basename(amostra_txt)}')
    q_data = compute_quali(amostra_txt)
    q_data = q_data[q_data['AREAP'].astype(str).str[:7].isin(list_muns)]
    print(f'  → {q_data["AREAP"].nunique()} APs')
    if len(q_data):
        all_quali.append(q_data)

# ─── Update PS3 num_people ────────────────────────────────────────────────────
print('\n=== Updating num_people_age_gender_AP_2010.csv ===')
num_path = f'{PS3_INPUT}/num_people_age_gender_AP_2010.csv'
existing_num = pd.read_csv(num_path, sep=';')
existing_areaps = set(existing_num['AREAP'].astype(str))

new_num = pd.concat(all_num, ignore_index=True)
new_num = new_num[~new_num['AREAP'].astype(str).isin(existing_areaps)]
print(f'  Adding {new_num["AREAP"].nunique()} new APs ({len(new_num)} rows)')
pd.concat([existing_num, new_num], ignore_index=True).to_csv(num_path, sep=';', index=False)
print(f'  Saved.')

# ─── Update PS3 qualification ─────────────────────────────────────────────────
print('\n=== Updating qualification_APs_2010.csv ===')
quali_path = f'{PS3_INPUT}/qualification_APs_2010.csv'
existing_quali = pd.read_csv(quali_path)
existing_codes = set(existing_quali['code'].astype(str))

new_wide = quali_to_ps3(pd.concat(all_quali, ignore_index=True))
new_wide['code'] = new_wide['code'].astype(str)
new_wide = new_wide[~new_wide['code'].isin(existing_codes)]
print(f'  Adding {len(new_wide)} new APs')
pd.concat([existing_quali, new_wide], ignore_index=True).to_csv(quali_path, index=False)
print(f'  Saved.')

print('\nAll done.')