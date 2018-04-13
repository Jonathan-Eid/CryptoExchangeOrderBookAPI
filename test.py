import websocketClients
import websocket
import json
from queue import Queue
import threading

#gdax = websocket.create_connection("wss://api.bitfinex.com/ws/2")
#gdaxorder = websocketClients.bitfenixRequest("subscribe", "BTC-USD").toJson()

boo = True
q = Queue()
#gdax.send(json.dumps(gdaxorder))
gdax = websocketClients.GDAXClient()
gdax.connect()
gdax.retrieveOrderBook("BTC-USD")
t1 = threading.Thread(target=gdax.orderbookUpdates, args=(q,))
t1.daemon = True
t1.start()

def printQ(o):
    while o:
        print(q.get())
        q.task_done()

t2 = threading.Thread(target=printQ, args=(boo, ))
t2.start()
gdax.disconnect()
q.join()
boo = False

gdax = websocket.create_connection("wss://ws-feed.gdax.com")
gdaxorder = websocketClients.gdaxRequest("subscribe", "BTC-USD").toJson()

gdax.send(json.dumps(gdaxorder))
print(gdax.recv())
print(gdax.recv())
print(gdax.recv())
print(gdax.recv())
print(gdax.recv())
print(gdax.recv())


#gdax.disconnect()



