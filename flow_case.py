from prefect import task, flow

from extract import get_raw_dict
from transform import get_tablon
from load import load_tablon
from prefect.logging import get_run_logger

@flow(name='logger-etl-btc')
def flow_case():
    log = get_run_logger()
    try:
        raw_data = _extract()
        data = _transform(raw_data)
        load(data)
    except Exception as e:
        log.error(e)

@task(name='logger-etl-btc', retries = 3, retry_delay_seconds=120)
def _extract():
    raw_dict = get_raw_dict()
    return raw_dict

@task(name='logger-etl-btc')
def _transform(raw_dict):
    tablon = get_tablon(raw_dict)
    
    return tablon

@task(name='logger-etl-btc')
def load(data):
    load_tablon(data)

if __name__ == '__main__':
    flow_case()