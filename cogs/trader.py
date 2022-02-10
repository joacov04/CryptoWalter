import discord
from discord.ext import commands
from binance.client import Client
from binance.enums import *
import dbManagement

class Trader(commands.Cog):

    def __init__(self, client):
        self.client = client


    def get_client(self, user):
        data = dbManagement.get_api(user)
        try:
            binance_client = Client(data[2], data[3])
            return binance_client
        except Exception as e:
            err = "ERROR - {}".format(e)
            return err

    def embSpotOrder(self, order):
        if 'APIError' in order:
            color = 0xff0000
            emb = discord.Embed(title = str(order), color=color)
            return emb

        elif order['side'] == 'SELL':
            color = 0x9e2626

        else:
            color = 0x269e46
        emb = discord.Embed(title=order['symbol'] + ' ' + order['side'], color=color)
        emb.add_field(name='Quantity', value=str(order['executedQty']))
        emb.add_field(name='Cummulative quote quantity', value=str(order['cummulativeQuoteQty']))
        emb.add_field(name='Price', value=str(order['fills'][0]['price']))
        return emb

    def set_spot_side(self, side: str):
        if 'BUY' in side.upper():
            side = SIDE_BUY
        if 'SELL' in side.upper():
            side = SIDE_SELL
        if 'BOTH' in side.upper():
            side = BOTH
        return side

    def embSinglePrice(self, price):
        sign = ''
        if 'APIError' in price:
            color = 0xff0000
            emb = discord.Embed(title = str(price), color=color)
            return emb

        elif float(price['priceChange']) < 0.0:
            color = 0x9e2626

        else:
            color = 0x269e46
            sign = '+'

        if float(price['lastPrice']) >= 5.0:
            fancy_price = str(round(float(price['lastPrice']), 2))
        else:
            fancy_price = str(round(float(price['lastPrice']), 4))

        fancy_percent = sign + str(round(float(price['priceChangePercent']), 2)) + '%'
        emb = discord.Embed(title=price['symbol'], color=color)
        emb.add_field(name='Price', value=fancy_price)
        emb.add_field(name='24h Change', value=fancy_percent)
        return emb


    def sendSpotOrder(self, client, symb, side, quantity, order_type=ORDER_TYPE_MARKET):
        '''Creates a new spot order, MARKET by default,
        side must be a string containing the word sell or buy'''
        spot_side = Trader.set_spot_side(self, side)

        try:
            order = client.create_order(symbol=symb, side=spot_side, type=order_type, quoteOrderQty=quantity)
            return order

        except Exception as e:
            err = "Binance error - {}".format(e)
            return err

    def getAccApiStats(self, client):
        try:
            api = client.get_account_api_trading_status()
            return api

        except Exception as e:
            err = "Binance error - {}".format(e)
            return err

    def getSymPrice(self, client, symb):
        try:
            price = client.get_ticker(symbol=symb)
            return price

        except Exception as e:
            err = f'Binance error - {e}'
            return err


    #Commands
    @commands.command()
    async def ping(self, ctx):
        username = ctx.author.name + '#' + str(ctx.author.discriminator) 
        binance_client = Trader.get_client(self, username)
        api = Trader.getAccApiStats(self, binance_client)
        await ctx.send(str(api))

    @commands.command()
    async def spot(self, ctx, side: str, symb: str,  ammount: float):
        username = ctx.author.name + '#' + str(ctx.author.discriminator) 
        binance_client = Trader.get_client(self, username)
        order = Trader.sendSpotOrder(self, binance_client, symb.upper(), side, ammount)
        await ctx.send(embed=Trader.embSpotOrder(self, order))

    @commands.command()
    async def p(self, ctx, symb: str):
        username = ctx.author.name + '#' + str(ctx.author.discriminator) 
        binance_client = Trader.get_client(self, username)
        price = Trader.getSymPrice(self, binance_client, symb.upper())
        msg = Trader.embSinglePrice(self, price)
        await ctx.send(embed=msg)




def setup(client):
    client.add_cog(Trader(client))
