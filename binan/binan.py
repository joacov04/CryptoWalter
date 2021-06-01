import os
from binance.client import Client

api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')

client = Client(api_key, api_secret)

tickers = client.get_all_tickers()


# Aplicar busqueda binaria
def getPrice(symbol):
    tickers = client.get_all_tickers()
    for item in tickers:
        if item['symbol'] == symbol:
            return item['price']


list = []
for i in tickers:
    list.append(i['symbol'])

