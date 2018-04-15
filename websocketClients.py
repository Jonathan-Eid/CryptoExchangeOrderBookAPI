import json
from queue import Queue
from websocket import create_connection
import orders
import orderbook
import threading

class gdaxRequest:
    def __init__(self, type, tickers):
        self.type = type
        self.tickers = tickers

    def toJson(self):
        jsonStr = """
                {
                    "type": "%s",
                    "channels": [{ "name": "level2", "product_ids": ["%s"] }]
                }
                """ % (self.type, self.tickers)
        return json.loads(jsonStr)

class bitfenixRequest:
    def __init__(self, type, tickers):
        self.type = type
        self.tickers = tickers.replace("-", "")

    def toJson(self):
        jsonStr = """
                {
                    "event":"%s",
                    "channel":"book",
                    "pair":"%s"
                }
                """ % (self.type, self.tickers)
        return json.loads(jsonStr)


class Client:
    def __init__(self, url):
        self.url = url
        self.connection = None

    def connect(self):
        if self.connection is None:
            self.connection = create_connection(self.url)
            print("Connection successful!")
        else:
            print("Already connected!")

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            print("Disconnected successfully!")
        else:
            print("Already disconnected!")

    def isConnected(self):
            if self.connection is not None:
                return self.connection.connected
            else:
                return False

class GDAXClient(Client):
    def __init__(self,url="wss://ws-feed.gdax.com"):
        Client.__init__(self, url)
        self.url = url

    def connect(self):
        if self.connection is None:
            self.connection = create_connection(self.url)
            print("Connected to GDAX!")
        else:
            print("Already connected!")

    def retrieveOrderBook(self, tickers):
        if self.connection is not None:
            self.connection.send(json.dumps(gdaxRequest("subscribe", tickers).toJson()))
            snapshot = orders.createGDAXOrdersfromSnapshot(json.loads(self.connection.recv()))
            updateThread = threading.Thread(target=self.orderbookUpdates)
            updateThread.daemon = True
            updateThread.start()
            orderbook.addOrders(snapshot)
        else:
            print("Connection needs to be established first!")

    def orderbookUpdates(self):
        if self.isConnected():
            while self.isConnected():
                update = json.loads(self.connection.recv())
                if update["type"] == 'l2update':
                    if update["changes"][0][2] != "0":
                        update = orders.createGDAXOrderfromUpdate(update)
                        orderbook.addUpdates(update)

        else:
            print("Connection needs to be established first!")


class BitFenixClient(Client):
    def __init__(self,url="wss://api.bitfinex.com/ws/2"):
        Client.__init__(self, url)
        self.url = url
        self.tickers = None

    def connect(self):
        if self.connection is None:
            self.connection = create_connection(self.url)
            print("Connected to BitFinex!")
        else:
            print("Already connected!")

    def retrieveOrderBook(self, tickers):
        if self.isConnected():
            self.tickers = tickers
            self.connection.send(json.dumps(bitfenixRequest("subscribe", tickers).toJson()))
            self.connection.recv()
            self.connection.recv()
            snapshot = orders.createBitFinexOrderfromSnapshot(json.loads(self.connection.recv()), tickers)
            updateThread = threading.Thread(target=self.orderbookUpdates)
            updateThread.daemon = True
            updateThread.start()
            orderbook.addOrders(snapshot)
        else:
            print("Connection needs to be established first!")

    def orderbookUpdates(self):
        if self.isConnected():
            while self.isConnected():
                update = json.loads(self.connection.recv())
                if not isinstance(update[1],str):
                    if update[1][1] is not 0:
                        update = orders.createBitFinexOrderfromUpdate(update,self.tickers)
                        orderbook.addUpdates(update)
        else:
            print("Connection needs to be established first!")

