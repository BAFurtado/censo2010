import pandas as pd

# Restricting everything to list of 333 municipalities of ACPs (Areas de Concentracao de Populacao/IBGE 2015)
muns = pd.read_csv('mun_of_interest.csv', sep=';')
list_muns = list(muns.cod_mun)
list_muns = [str(m) for m in list_muns]

# Getting string of states that include all municipalities of interest
states = list(set([state[:2] for state in list_muns]))
states_link = pd.read_csv('data/STATES_ID_NUM.csv', sep=';')
states_link = list(states_link[states_link['nummun'].astype(str).isin(states)].loc[:, 'codmun'])

# Restricting mapping from sectors to weighted areas for municipalities of interest only
aps = pd.read_csv('data/areas_ponderacao_setores.csv', encoding='utf-16', sep='\t')
aps['mun'] = aps.loc[:, 'AREAP'].astype(str).str[:7]
aps = aps[aps['mun'].isin(list_muns)]
aps = aps[['AREAP', 'setor']]
aps.columns = ['AREAP', 'Cod_setor']
