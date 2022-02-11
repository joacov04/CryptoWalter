import discord
from discord.ext import commands
from binance.client import Client
from binance.enums import *
import dbManagement

class Trader(commands.Cog):

    def __init__(self, client):
        self.client = client


    def get_client(self, id):
        data = dbManagement.get_api(id)
        if data is None:
            raise Exception("You're not logged in with your Binance account.")
        binance_client = Client(data[1], data[2])
        return binance_client

    def embSpotOrder(self, order):
        if 'APIError' in order or 'ERROR' in order:
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
            raise Exception(err)


    def getSymPrice(self, client, symb):
        try:
            price = client.get_ticker(symbol=symb)
            return price

        except Exception as e:
            err = f'Binance error - {e}'
            raise Exception(err)


    #Commands
    ping_help = 'Pong!'
    @commands.command(help=ping_help)
    async def ping(self, ctx):
        await ctx.send('Pong!')

    spot_help = 'Makes a spot order, being <side> buy or sell, <symbol> the pair and <amount> the amount of crypto to operate'
    spot_brief = 'Makes a spot order.'
    @commands.command(help=spot_help, brief=spot_brief)
    async def spot(self, ctx, side: str, symbol: str,  amount: float):
        id = ctx.author.id
        try:
            binance_client = Trader.get_client(self, id)
            order = Trader.sendSpotOrder(self, binance_client, symbol.upper(), side, amount)
            await ctx.send(embed=Trader.embSpotOrder(self, order))
        except Exception as e:
            await ctx.send(e)

    p_help = 'Sends the price of the <symbol> pair.'
    p_brief = 'Sends a certain crypto price.'
    @commands.command(help=p_help, brief=p_brief)
    async def p(self, ctx, symbol: str):
        id = ctx.author.id

        try:
            binance_client = Trader.get_client(self, 517016219002339329)
            price = Trader.getSymPrice(self, binance_client, symbol.upper())
            msg = Trader.embSinglePrice(self, price)
            await ctx.send(embed=msg)

        except Exception as e:
            await ctx.send(str(e))

    login_help = "USE THIS COMMAND VIA DM. Log in with your Binance account, send your api_key in the <api> argument and your secret_key in the <secret_key> argument."
    login_brief = 'ONLY VIA DM - login to your Binance account'
    @commands.command(help=login_help, brief=login_brief)
    async def login(self, ctx, api, secret_key):
        id = ctx.author.id
        if ctx.guild is not None:
            await ctx.send('Please use this command only via DM. For your on safety :sunglasses:')
        else:
            if dbManagement.get_api(id) is None:
                try: 
                    binance_client = Client(api, secret_key)                
                    info = binance_client.get_account()
                    dbManagement.insert_user(id, api, secret_key)
                    await ctx.send(f'Succesfully logged in.')
                except:
                    await ctx.send('Credentials are wrong. Try again!')
                
            else:
                await ctx.send(f"You're already logged in {ctx.author.name}!")




def setup(client):
    client.add_cog(Trader(client))
