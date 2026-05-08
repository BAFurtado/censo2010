#!/usr/bin/env python3
"""
Rebuild PS3/input/shapes/2010/areas/{UF}.shp for all states using the
updated mun_of_interest.csv.

Source: censo2010/data/areas/{num}_all_muns.shp  (AREAP, geometry)
Target: PS3/input/shapes/2010/areas/{UF}.shp     (id, mun_code, geometry)
"""

import os
import geopandas as gpd
import pandas as pd

AREAS_DIR = '/home/furtado/MyModels/censo2010/data/areas'
PS3_SHAPES_DIR = '/home/furtado/MyModels/PS3/input/shapes/2010/areas'
MUN_OF_INTEREST = '/home/furtado/MyModels/censo2010/mun_of_interest.csv'
STATES_MAP = '/home/furtado/MyModels/PS3/input/STATES_ID_NUM.csv'

# Build numeric → UF lookup
states_df = pd.read_csv(STATES_MAP, sep=';')
num_to_uf = dict(zip(states_df['nummun'].astype(str), states_df['codmun']))

# Load selected municipality codes from updated mun_of_interest
muns = pd.read_csv(MUN_OF_INTEREST, sep=';')
selected_mun_codes = set(muns['cod_mun'].astype(str).unique())

total_added = 0

for fname in sorted(os.listdir(AREAS_DIR)):
    if not fname.endswith('_all_muns.shp'):
        continue

    state_num = fname.split('_')[0]
    uf = num_to_uf.get(state_num)
    if uf is None:
        print(f'  WARNING: no UF mapping for state {state_num}, skipping')
        continue

    src_path = os.path.join(AREAS_DIR, fname)
    dst_path = os.path.join(PS3_SHAPES_DIR, f'{uf}.shp')

    gdf = gpd.read_file(src_path)
    gdf['AREAP'] = gdf['AREAP'].astype(str)
    gdf['mun_code'] = gdf['AREAP'].str[:7]

    # Filter to municipalities in updated mun_of_interest
    filtered = gdf[gdf['mun_code'].isin(selected_mun_codes)].copy()
    filtered = filtered.rename(columns={'AREAP': 'id'})
    filtered = filtered[['id', 'mun_code', 'geometry']]

    if len(filtered) == 0:
        print(f'  {uf} ({state_num}): no selected municipalities — skipping')
        continue

    filtered.to_file(dst_path)
    total_added += len(filtered)
    print(f'  {uf} ({state_num}): {len(filtered)} APs written to {uf}.shp')

print(f'\nDone. {total_added} total APs written across all states.')