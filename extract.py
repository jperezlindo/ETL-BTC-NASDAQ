import requests
import yfinance as yf
import pandas as pd
from prefect.logging import get_run_logger

from variables import tickers, today

# log = get_run_logger()

def _get_tickers():
    try:
        raw_dict = {}
        for ticker in tickers:
            tk = yf.Ticker(ticker)
            raw_df = pd.DataFrame(tk.history(period='1d'))
            raw_df.columns = raw_df.columns.str.lower()
            raw_df = raw_df[['open', 'high', 'low', 'close']]
            raw_dict[ticker] = raw_df

        return raw_dict
    except Exception as e:
        print(e)
        # log.error(e)

def _get_btc_price():
    try:
        url = 'https://api.coinbase.com/v2/prices/spot?currency=USD'
        response = requests.get(url)
        assert response.status_code == 200, 'Error al recuperar los datos de COINBASE'
        raw = response.json()
        btc_price = float(raw['data']['amount'])
        btc_index = pd.to_datetime(today).tz_localize('America/New_York')
        btc_dict = {'Date': [btc_index], 'btc_price': [btc_price]}
        btc_df = pd.DataFrame(btc_dict)
        btc_df.set_index('Date', inplace=True)

        return btc_df
    except AssertionError as e:
        print(e)
        # log.error(e)

def get_raw_dict():
    try:
        raw_dict = _get_tickers()
        btc_df = _get_btc_price()
        if raw_dict is not None:
            raw_dict['btc_usd'] = btc_df

            return raw_dict
    except Exception as e:
        print(e)
        # log.error(e)

if __name__ == '__main__':
    raw_dict = get_raw_dict()


