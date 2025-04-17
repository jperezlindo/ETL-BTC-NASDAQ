
import pandas as pd
import numpy as np
from prefect.logging import get_run_logger

from variables import tickers

# Crea los valores para 'dif_apert_cierre', 'rango_dia', 'signo_dia']
def _create_values_for_ticker(raw_dict):
    # new_dict = {}
    for ticker in tickers:
        df = raw_dict[ticker]
        df['dif_apert_cierre'] = df['open'] - df['close']
        df['rango_dia'] = df['high'] - df['low']
        df['signo_dia'] = np.where(df['dif_apert_cierre'] > 0.0, '+',np.where(df['dif_apert_cierre'] < 0.0, '-', '0'))
        df = df[['close', 'dif_apert_cierre', 'rango_dia', 'signo_dia']]
        df.columns = map(lambda x: f'{ticker}_{x}', df.columns.to_list())
        raw_dict[ticker] = df
    return raw_dict

def _create_tablon(new_dict):
    dfs_list = new_dict.values()
    tablon = pd.concat(dfs_list, axis=1)
    
    return tablon

def  get_tablon(raw_dict):
    log = get_run_logger()
    try:
        new_dict = _create_values_for_ticker(raw_dict)
        tablon = _create_tablon(new_dict)

        return tablon
    except Exception as e:
        log.error(e)

if __name__ == '__main__':
    pass
    # from extract import get_raw_dict
    # raw_dict = get_raw_dict()
    # tablon = get_tablon(raw_dict)
