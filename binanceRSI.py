import API_CHECKER
import json
import numpy
import pprint
import talib
import websocket
from binance.client import Client
from binance.enums import *
from decimal import Decimal

SOCKET = "wss://stream.binance.com:9443/ws/ethbusd@kline_1m"   ## ethbusd --> currency, 1m --> time

RSI_PERIOD = 14
RSI_OVERBOUGHT = 69.5     ## Check the RSI formula, then you can change them!
RSI_OVERSOLD = 30.5
TRADE_SYMBOL = 'ETHBUSD'
TRADE_QUANTITY = 0  ## How much coin will you buy?
precision = 6
price_str = '{:0.0{}f}'.format(TRADE_QUANTITY, precision)
price_deneme = float(TRADE_QUANTITY)
price_deneme2 = '{0:.8g}'.format(TRADE_QUANTITY)
TRADE_QUANTITY_CONVERTED = TRADE_QUANTITY * (0.001)
Real = TRADE_QUANTITY - TRADE_QUANTITY_CONVERTED
price_str_2 = '{:0.0{}f}'.format(Real, precision)
rounded_lot_size = round(Real, 5)

closes = []       ## Array for closed transactions.
in_position = False

client = Client(API_CHECKER.API_KEY, API_CHECKER.API_SECRET, tld='com')

info = client.get_symbol_info('ETHBUSD')      ## For viewing information on the console.
print(info)
print(client.get_asset_balance(asset='BUSD'))     ## Our assets.
## Function to create a market order. You can change the order types if you wish.
def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("Order is sending!")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as a:
        print("Error occured --> - {}".format(a))    ## Show the error? (Why we could not buy?)
        return False
    return True


def on_open(ws):
    print('Connection Established!')


def on_close(ws):
    print('Bağlantı Lost!')


def on_message(ws, message):
    global closes, in_position

    print('Progressing...')
    json_message = json.loads(message)
    pprint.pprint(json_message)
    candle = json_message['k']
    close = candle['c']  ## Candle closing value.
    is_candle_closed = candle['x']
    if is_candle_closed:
        print("Candle closing value {}".format(close))
        closes.append(float(close))
        print("Closing")
        print(closes)

        if len(closes) > 45:        ## For better RSI calculations, we need a big number like 45. If not, calculations are not the exact RSI values because of period.
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("Calculated RSI values")
            print(rsi)
            last_rsi = rsi[-1]
            print("Current RSI {}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("Overbought Zone, SOLD!!!")

                    order_succeeded = order(SIDE_SELL, Real, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = False     ## That means we closed our position.
                else:
                    print("Overbought Zone, however we have no coins!!!")

            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("Oversold Zone, however we have already bought coins!!!")
                else:
                    print("Oversold Zone, BOUGHT!!!")

                    order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = True    ## We have a positin now.

## Websocket connection with on_message method.
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()    ## App works unless you close it.
