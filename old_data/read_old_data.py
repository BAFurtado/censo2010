import pandas as pd

ACP_CODES = pd.read_csv('old_data/ACPs_BR.csv', sep=';', header=0, decimal=',')
ACPS_MUN_CODES = pd.read_csv('old_data/ACPs_MUN_CODES.csv', sep=';', header=0, decimal=',')
STATES_CODES = pd.read_csv('old_data/STATES_ID_NUM.csv', sep=';', header=0, decimal=',')
mun_list = pd.read_csv('old_data/names_and_codes_municipalities.csv', header=0, sep=';', decimal=',')


def state_string(state, states_codes):
    state_id = states_codes.loc[states_codes['codmun'] == state]['nummun']
    return str(state_id.iloc[0])