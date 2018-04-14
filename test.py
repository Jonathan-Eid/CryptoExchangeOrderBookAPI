import websocketClients
import websocket
import json
from queue import Queue
import threading
import orderbook
import jsonout

gdax = websocketClients.GDAXClient()
gdax.connect()
bit = websocketClients.BitFenixClient()
bit.connect()
orders1 = bit.retrieveOrderBook("BTC-USD")
orders = gdax.retrieveOrderBook("BTC-USD")
orderbook.addOrders(orders1)
orderbook.addOrders(orders)





