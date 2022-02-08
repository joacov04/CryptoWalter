import discord
import os
from dotenv import load_dotenv
import binan

load_dotenv()
TOKEN = os.getenv('discord_secret')
client = discord.Client()

prefix = '='


def fancy_print(order):
    if order['side'] == 'SELL':
        color = 0x9e2626
    else:
        color = 0x269e46
    emb = discord.Embed(title=order['symbol'] + ' ' + order['side'], color=color)
    emb.add_field(name='Quantity', value=str(order['executedQty']))
    emb.add_field(name='Cummulative quote quantity', value=str(order['cummulativeQuoteQty']))
    emb.add_field(name='Price', value=str(order['fills'][0]['price']))
    return emb

@client.event
async def on_ready():
    print('Estoy vivo como {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(prefix):
        username = message.author.name + '#' + str(message.author.discriminator)
        binance_client = binan.get_client(username)
        binance_f_client = binan.get_f_client(username)
        if 'spotOrder' in message.content:
            content = message.content.replace(' ', '').split(',')

            order = binan.spotOrder(binance_client, content[1].upper(), content[2], float(content[3]))

            if 'APIError' in order:
                await message.reply('ERROR -' + order.split(':')[1])
            else:
                await message.reply(embed=fancy_print(order))

        if 'futuresOrder' in message.content:
            content = message.content.replace(' ', '').split(',')

            order = binan.execute_order(binance_f_client, _market=content[1].upper(), _side=content[2], _qty=float(content[3]))

            if 'APIError' in order:
                await message.reply('ERROR -' + order.split(':')[1])
            else:
                await message.reply(str(order))


client.run(TOKEN)
