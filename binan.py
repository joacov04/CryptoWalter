from binance.client import Client
import pprint
from binance.enums import *
import dbManagement
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *


def getPrice(symb):
    return client.get_avg_price(symbol=symb)


def get_client(user):
    data = dbManagement.get_api(user)
    try:
        client = Client(data[2], data[3])
        return client
    except Exception as e:
        err = "ERROR - {}".format(e)
        return err


def get_f_client(user):
    data = dbManagement.get_api(user)
    client = RequestClient(api_key=data[2], secret_key=data[3])
    return client


def set_spot_side(side: str):
    if 'BUY' in side.upper():
        side = SIDE_BUY
    if 'SELL' in side.upper():
        side = SIDE_SELL
    if 'BOTH' in side.upper():
        side = BOTH
    return side


def set_margin_side(side: str):
    if 'LONG' in side.upper():
        side = 'LONG'
    if 'SHORT' in side.upper():
        side = 'SHORT'
    return side


def spotOrder(client, symb, side, quantity, order_type=ORDER_TYPE_MARKET):
    '''Creates a new spot order, MARKET by default,
    side must be a string containing the word sell or buy'''
    spot_side = set_spot_side(side)

    try:
        order = client.create_order(symbol=symb, side=spot_side, type=order_type, quoteOrderQty=quantity)
        return order

    except Exception as e:
        err = "Error - {}".format(e)
        return err

def execute_order(client, _market="BTCUSDT", _type="MARKET", _side="BUY", _position_side="BOTH", _qty=1.0):
    '''To LONG _side must be BUY, to short it must be SELL'''
    client.post_order(symbol=_market,
                      ordertype=_type,
                      side=_side,
                      positionSide=_position_side,
                      quantity=_qty)


def change_leverage(client, symb, lever):
    try:
        result = client.futures_change_leverage(symbol=symb, leverage=int(lever))
        return result
    except Exception as e:
        err = "ERROR - {}".format(e)
        return err
