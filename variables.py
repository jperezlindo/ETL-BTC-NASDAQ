from datetime import date
# coNSULTAR EL SIQUIENTE ENLACE EN EL CASO DE QUE SE CACHEE LAS VARIABLES TODAY Y TICKERS
# https://docs.prefect.io/core/concepts/persistence.html#output-caching-based-on-a-file-target)

tickers = ['NVDA', 'TSLA', 'AMD', 'INTC', 'MSFT']
today = date.today().strftime('%Y-%m-%d')