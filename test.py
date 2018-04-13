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
orderbook.init()
orderbook.addOrders(orders1)
orderbook.addOrders(orders)
gdaxQ = Queue()
bitQ = Queue()
getGDAXUpdate = threading.Thread(target=gdax.orderbookUpdates, args=(gdaxQ,))
getGDAXUpdate.start()
getBitFinexUpdate = threading.Thread(target=bit.orderbookUpdates, args=(bitQ,))
getBitFinexUpdate.start()
orderbookUpdate1 = threading.Thread(target=orderbook.addUpdates, args=(gdaxQ,))
orderbookUpdate1.start()
orderbookUpdate2 = threading.Thread(target=orderbook.addUpdates, args=(bitQ,))
orderbookUpdate2.start()
orderbook.printBeforeFlush()




