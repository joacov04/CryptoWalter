# CryptoWalter - Discord bot written in python
This bot can be connected with a binance account via API to make spot trades from Discord. It also sends the price of the asked cryptocurrencies.

After clonning this repo:
install python3 and all the pip packages specified in requirements.txt
create a sqlite databse called data.db with a table called api, with three columns: user(int),
api_key(text), secret_api(text) 


Commands:

.p ADAUSDT  ->  Sends the price of the asked pair and the 24h Change.

.spot sell ADAUSDT 100  ->  Sells 100 dollars worth of ada, can also buy.

.ping  ->  Pong!
