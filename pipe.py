from binan import binan 

coin, pair = '', ''


async def findPrice(message):
    for i in binan.list:
        if message.content.upper() == i:
            await message.channel.send('{0:.5f}'.format(float(binan.getPrice(i.upper()))))


async def crypto(message):
    content = ''
    price = 0.0
    for i in binan.list:
        if 'BTCUSDT' in i or 'ETHUSDT' in i or 'ADAUSDT' in i or 'DOTUSDT' in i or 'BNBUSDT' in i or 'DOGEUSDT' in i or 'XRPUSDT' in i:
            price = binan.getPrice(i)
            content += ':dollar: ** '
            content += i.replace('USDT', '')
            content += '**'
            if float(price) < 5:
                price = '{0:.5f}'.format(float(price))
            else:
                price = '{0:.2f}'.format(float(price))
            content += f' = {price}'
            content += '\n'
            
    await message.channel.send(str(content))
    await message.channel.send('Fuente: https://binance.com')

    
